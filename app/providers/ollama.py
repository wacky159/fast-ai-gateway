"""
Ollama provider implementation.
"""

import json
import logging
import uuid
from typing import Any

from app.config import get_settings
from app.core.errors import InvalidModelOutputError, ProviderBadResponseError
from app.core.http import create_http_client
from app.providers.base import BaseProvider
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.common import UsageInfo

logger = logging.getLogger(__name__)


class OllamaProvider(BaseProvider):
    """Ollama API provider implementation."""

    def __init__(self) -> None:
        settings = get_settings()
        self._model = settings.ai_model
        self._client = create_http_client(settings.ollama_base_url)

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def model(self) -> str:
        return self._model

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Process a chat completion request via Ollama API."""
        # Convert messages to Ollama format
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        # Add JSON format instruction if requested
        if request.response_format == "json":
            system_msg = next(
                (m for m in messages if m["role"] == "system"), None
            )
            json_instruction = "\n\nYou MUST respond with valid JSON only. No additional text."
            if system_msg:
                system_msg["content"] += json_instruction
            else:
                messages.insert(0, {"role": "system", "content": json_instruction.strip()})

        # Build Ollama request
        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        }

        response = await self._client.post("/api/chat", payload)

        # Parse response
        message = response.get("message", {})
        content = message.get("content", "")

        # Extract usage info if available
        usage = UsageInfo(
            input_tokens=response.get("prompt_eval_count"),
            output_tokens=response.get("eval_count"),
            total_tokens=None,
        )
        if usage.input_tokens and usage.output_tokens:
            usage.total_tokens = usage.input_tokens + usage.output_tokens

        return ChatResponse(
            id=f"chatcmpl_{uuid.uuid4().hex[:12]}",
            provider=self.name,
            model=self._model,
            output=content,
            usage=usage,
        )

    async def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Process a text analysis request via Ollama API."""
        # Build the analysis prompt
        prompt = self._build_analyze_prompt(request)

        # Build Ollama request
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": self._get_analyze_system_prompt(request)},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for consistent output
                "num_predict": 512,
            },
        }

        response = await self._client.post("/api/chat", payload)

        # Parse response
        message = response.get("message", {})
        content = message.get("content", "")

        # Parse JSON from model output
        result = self._parse_analyze_output(content, request)

        return AnalyzeResponse(
            provider=self.name,
            model=self._model,
            label=result.get("label"),
            score=result.get("score"),
            summary=result.get("summary"),
            extras=result.get("extras", {}),
        )

    def _get_analyze_system_prompt(self, request: AnalyzeRequest) -> str:
        """Generate the system prompt for analysis."""
        fields = []
        if request.options.need_label:
            fields.append('"label": string (POSITIVE, NEGATIVE, or NEUTRAL)')
        if request.options.need_score:
            fields.append('"score": number between 0.0 and 1.0')
        if request.options.need_summary:
            fields.append('"summary": string (brief summary)')
        if request.options.extra_fields:
            for field in request.options.extra_fields:
                if field == "keywords":
                    fields.append('"keywords": array of strings')
                elif field == "category":
                    fields.append('"category": string')
                else:
                    fields.append(f'"{field}": string or array')

        fields_str = ", ".join(fields)

        return f"""You are a text analysis assistant. Analyze the given text and respond with ONLY valid JSON.
Do NOT include any text before or after the JSON.
Do NOT use markdown code blocks.

Required JSON format:
{{{fields_str}}}

If a field cannot be determined, use null for that field."""

    def _build_analyze_prompt(self, request: AnalyzeRequest) -> str:
        """Build the user prompt for analysis."""
        return f"Analyze the following text:\n\n{request.text}"

    def _parse_analyze_output(
        self, content: str, request: AnalyzeRequest
    ) -> dict[str, Any]:
        """Parse the model's JSON output."""
        # Try to extract JSON from the content
        content = content.strip()

        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            # Remove first and last lines (code block markers)
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines)

        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse model output as JSON: {e}")
            logger.debug(f"Raw content: {content}")
            raise InvalidModelOutputError(
                f"Model output is not valid JSON: {e}"
            ) from e

        # Validate and normalize the result
        normalized: dict[str, Any] = {}

        if request.options.need_label:
            label = result.get("label")
            if isinstance(label, str):
                normalized["label"] = label.upper()
            else:
                normalized["label"] = None

        if request.options.need_score:
            score = result.get("score")
            if isinstance(score, (int, float)) and 0 <= score <= 1:
                normalized["score"] = float(score)
            else:
                normalized["score"] = None

        if request.options.need_summary:
            normalized["summary"] = result.get("summary")

        # Handle extra fields
        if request.options.extra_fields:
            extras = {}
            for field in request.options.extra_fields:
                if field in result:
                    extras[field] = result[field]
            normalized["extras"] = extras

        return normalized
