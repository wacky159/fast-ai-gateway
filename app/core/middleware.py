"""
FastAPI middleware for request tracking and logging.
"""

import logging
import time
import uuid
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import log_with_context, request_id_var

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware to inject request_id into each request."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        # Generate or extract request_id
        request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:12]}"

        # Store in context variable for logging
        token = request_id_var.set(request_id)

        try:
            response = await call_next(request)
            # Add request_id to response headers
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            request_id_var.reset(token)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request/response details."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        latency_ms = (time.perf_counter() - start_time) * 1000

        log_with_context(
            logger,
            logging.INFO,
            f"{request.method} {request.url.path}",
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            latency_ms=round(latency_ms, 2),
        )

        return response
