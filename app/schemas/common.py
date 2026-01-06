"""
Common schemas shared across the API.
"""

from pydantic import BaseModel, Field


class UsageInfo(BaseModel):
    """Token usage information."""

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


class ErrorDetail(BaseModel):
    """Error detail in API response."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    request_id: str = Field(..., description="Request ID for tracing")


class ErrorResponse(BaseModel):
    """Standardized error response format."""

    error: ErrorDetail
