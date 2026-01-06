"""
Provider factory for creating AI provider instances.
"""

from functools import lru_cache

from app.config import get_settings
from app.providers.base import BaseProvider
from app.providers.ollama import OllamaProvider
from app.providers.openai import OpenAIProvider


@lru_cache
def get_provider() -> BaseProvider:
    """
    Get the configured AI provider instance.

    Returns:
        The appropriate provider based on AI_PROVIDER environment variable.

    Raises:
        ValueError: If an unsupported provider is configured.
    """
    settings = get_settings()
    provider_name = settings.ai_provider.lower()

    if provider_name == "ollama":
        return OllamaProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    else:
        raise ValueError(f"Unsupported AI provider: {provider_name}")
