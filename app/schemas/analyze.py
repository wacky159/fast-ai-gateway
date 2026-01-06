"""
Analyze endpoint request/response schemas.
"""

from typing import Any

from pydantic import BaseModel, Field


class AnalyzeOptions(BaseModel):
    """Options for text analysis."""

    need_summary: bool = Field(default=True, description="Include summary in response")
    need_label: bool = Field(default=True, description="Include sentiment label")
    need_score: bool = Field(default=True, description="Include confidence score")
    extra_fields: list[str] = Field(
        default_factory=list,
        description="Additional fields to extract (e.g., 'keywords', 'category')",
    )


class AnalyzeRequest(BaseModel):
    """Request body for POST /v1/analyze."""

    text: str = Field(..., min_length=1, description="Text content to analyze")
    options: AnalyzeOptions = Field(
        default_factory=AnalyzeOptions, description="Analysis options"
    )


class AnalyzeResponse(BaseModel):
    """Response body for POST /v1/analyze."""

    provider: str = Field(..., description="AI provider used")
    model: str = Field(..., description="Model used for analysis")
    label: str | None = Field(
        default=None, description="Sentiment label (e.g., POSITIVE, NEGATIVE, NEUTRAL)"
    )
    score: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Confidence score"
    )
    summary: str | None = Field(default=None, description="Summary of the content")
    extras: dict[str, Any] = Field(
        default_factory=dict, description="Additional extracted fields"
    )
