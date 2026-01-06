"""
Custom exception classes and error handling utilities.
"""

from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    """Standardized error codes for API responses."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    PROVIDER_TIMEOUT = "PROVIDER_TIMEOUT"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    PROVIDER_BAD_RESPONSE = "PROVIDER_BAD_RESPONSE"
    INVALID_MODEL_OUTPUT = "INVALID_MODEL_OUTPUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class GatewayError(Exception):
    """Base exception for all gateway errors."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(GatewayError):
    """Raised when request validation fails."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR,
            message=message,
            status_code=422,
            details=details,
        )


class ProviderTimeoutError(GatewayError):
    """Raised when the upstream provider times out."""

    def __init__(self, message: str = "Upstream provider timeout") -> None:
        super().__init__(
            code=ErrorCode.PROVIDER_TIMEOUT,
            message=message,
            status_code=504,
        )


class ProviderUnavailableError(GatewayError):
    """Raised when the upstream provider is unavailable."""

    def __init__(self, message: str = "Upstream provider unavailable") -> None:
        super().__init__(
            code=ErrorCode.PROVIDER_UNAVAILABLE,
            message=message,
            status_code=503,
        )


class ProviderBadResponseError(GatewayError):
    """Raised when the upstream provider returns an invalid response."""

    def __init__(self, message: str = "Upstream provider returned bad response") -> None:
        super().__init__(
            code=ErrorCode.PROVIDER_BAD_RESPONSE,
            message=message,
            status_code=502,
        )


class InvalidModelOutputError(GatewayError):
    """Raised when the model output cannot be parsed as expected."""

    def __init__(self, message: str = "Model output could not be parsed") -> None:
        super().__init__(
            code=ErrorCode.INVALID_MODEL_OUTPUT,
            message=message,
            status_code=502,
        )
