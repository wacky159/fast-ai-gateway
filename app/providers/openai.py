"""
OpenAI provider implementation (stub for future use).
"""

from app.config import get_settings
from app.core.errors import GatewayError, ErrorCode
from app.providers.base import BaseProvider
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.schemas.chat import ChatRequest, ChatResponse


class OpenAIProvider(BaseProvider):
    """OpenAI API provider implementation (stub)."""

    def __init__(self) -> None:
        settings = get_settings()
        self._model = settings.ai_model
        self._api_key = settings.openai_api_key
        self._base_url = settings.openai_base_url

    @property
    def name(self) -> str:
        return "openai"

    @property
    def model(self) -> str:
        return self._model

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Process a chat completion request via OpenAI API."""
        raise GatewayError(
            code=ErrorCode.INTERNAL_ERROR,
            message="OpenAI provider is not yet implemented",
            status_code=501,
        )

    async def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Process a text analysis request via OpenAI API."""
        raise GatewayError(
            code=ErrorCode.INTERNAL_ERROR,
            message="OpenAI provider is not yet implemented",
            status_code=501,
        )
