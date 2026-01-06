"""
Pytest configuration and fixtures.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.providers.base import BaseProvider
from app.providers.factory import get_provider
from app.schemas.analyze import AnalyzeResponse
from app.schemas.chat import ChatResponse
from app.schemas.common import UsageInfo


class MockProvider(BaseProvider):
    """Mock provider for testing."""

    @property
    def name(self) -> str:
        return "mock"

    @property
    def model(self) -> str:
        return "mock-model"

    async def chat(self, request) -> ChatResponse:
        return ChatResponse(
            id="chatcmpl_test123",
            provider=self.name,
            model=self.model,
            output="This is a mock response.",
            usage=UsageInfo(input_tokens=10, output_tokens=20, total_tokens=30),
        )

    async def analyze(self, request) -> AnalyzeResponse:
        return AnalyzeResponse(
            provider=self.name,
            model=self.model,
            label="POSITIVE",
            score=0.95,
            summary="This is a mock summary.",
            extras={"keywords": ["mock", "test"]},
        )


@pytest.fixture
def mock_provider() -> MockProvider:
    """Create a mock provider instance."""
    return MockProvider()


@pytest.fixture
def client(mock_provider: MockProvider) -> Generator[TestClient, None, None]:
    """Create a test client with mocked provider."""
    app.dependency_overrides[get_provider] = lambda: mock_provider
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
