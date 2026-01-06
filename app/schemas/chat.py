"""
Chat endpoint request/response schemas.
"""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import UsageInfo


class ChatMessage(BaseModel):
    """A single message in a chat conversation."""

    role: Literal["system", "user", "assistant"] = Field(
        ..., description="The role of the message author"
    )
    content: str = Field(..., description="The content of the message")


class ChatRequest(BaseModel):
    """Request body for POST /v1/chat."""

    messages: list[ChatMessage] = Field(
        ..., min_length=1, description="List of messages in the conversation"
    )
    temperature: float = Field(
        default=0.2, ge=0.0, le=2.0, description="Sampling temperature"
    )
    max_tokens: int = Field(
        default=256, ge=1, le=4096, description="Maximum tokens to generate"
    )
    response_format: Literal["text", "json"] = Field(
        default="text", description="Response format (text or JSON)"
    )


class ChatResponse(BaseModel):
    """Response body for POST /v1/chat."""

    id: str = Field(..., description="Unique identifier for this completion")
    provider: str = Field(..., description="AI provider used")
    model: str = Field(..., description="Model used for generation")
    output: str = Field(..., description="Generated output text")
    usage: UsageInfo = Field(
        default_factory=UsageInfo, description="Token usage statistics"
    )
