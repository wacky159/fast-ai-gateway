"""
Text analysis endpoint.
"""

from fastapi import APIRouter, Depends

from app.providers.base import BaseProvider
from app.providers.factory import get_provider
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse

router = APIRouter(prefix="/v1", tags=["Analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    request: AnalyzeRequest,
    provider: BaseProvider = Depends(get_provider),
) -> AnalyzeResponse:
    """
    Text analysis endpoint.

    Analyzes the given text and returns structured results including
    sentiment label, confidence score, summary, and optional extra fields.
    """
    return await provider.analyze(request)
