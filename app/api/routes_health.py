"""
Health check endpoint.
"""

from fastapi import APIRouter

from app.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns the service status, current provider, model, and version.
    """
    settings = get_settings()

    return HealthResponse(
        status="ok",
        provider=settings.ai_provider,
        model=settings.ai_model,
        version=settings.service_version,
    )
