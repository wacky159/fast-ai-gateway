"""
Abstract base class for AI providers.
"""

from abc import ABC, abstractmethod

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.schemas.chat import ChatRequest, ChatResponse


class BaseProvider(ABC):
    """Abstract base class defining the provider interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        ...

    @property
    @abstractmethod
    def model(self) -> str:
        """Return the current model name."""
        ...

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat completion request.

        Args:
            request: The chat request with messages and parameters.

        Returns:
            ChatResponse with the generated output.
        """
        ...

    @abstractmethod
    async def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """
        Process a text analysis request.

        Args:
            request: The analyze request with text and options.

        Returns:
            AnalyzeResponse with structured analysis results.
        """
        ...
