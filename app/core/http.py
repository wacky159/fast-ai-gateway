"""
HTTP client wrapper with timeout and error handling.
"""

from typing import Any

import httpx

from app.config import get_settings
from app.core.errors import ProviderTimeoutError, ProviderUnavailableError


class HttpClient:
    """Async HTTP client with built-in timeout and error handling."""

    def __init__(self, base_url: str, timeout: float | None = None) -> None:
        settings = get_settings()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout or settings.request_timeout_seconds

    async def post(
        self,
        path: str,
        json_data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a POST request and return JSON response."""
        url = f"{self.base_url}{path}"
        request_headers = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=json_data,
                    headers=request_headers,
                )
                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(f"Request to {url} timed out") from e

        except httpx.ConnectError as e:
            raise ProviderUnavailableError(f"Cannot connect to {url}") from e

        except httpx.HTTPStatusError as e:
            raise ProviderUnavailableError(
                f"Provider returned status {e.response.status_code}"
            ) from e


def create_http_client(base_url: str, timeout: float | None = None) -> HttpClient:
    """Factory function to create an HTTP client."""
    return HttpClient(base_url, timeout)
