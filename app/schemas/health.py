"""
Health endpoint schema.
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response body for GET /health."""

    status: str = Field(..., description="Service status")
    provider: str = Field(..., description="Current AI provider")
    model: str = Field(..., description="Current model")
    version: str = Field(..., description="Service version")
