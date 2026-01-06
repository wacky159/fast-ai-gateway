"""
Application configuration using pydantic-settings.
All configuration is driven by environment variables.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Provider settings
    ai_provider: Literal["ollama", "openai"] = "ollama"
    ai_model: str = "gemma3:1b"

    # Ollama settings
    ollama_base_url: str = "http://localhost:11434"

    # OpenAI settings (for future use)
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"

    # Request settings
    request_timeout_seconds: int = 30

    # Logging settings
    log_level: str = "INFO"

    # Service metadata
    service_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
