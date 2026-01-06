"""
Chat completion endpoint.
"""

from fastapi import APIRouter, Depends

from app.providers.base import BaseProvider
from app.providers.factory import get_provider
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/v1", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    provider: BaseProvider = Depends(get_provider),
) -> ChatResponse:
    """
    Chat completion endpoint.

    Sends messages to the configured AI provider and returns the response.
    """
    return await provider.chat(request)
