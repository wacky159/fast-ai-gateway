"""
FastAPI AI Provider Gateway - Main Application Entry Point.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes_analyze import router as analyze_router
from app.api.routes_chat import router as chat_router
from app.api.routes_health import router as health_router
from app.config import get_settings
from app.core.errors import GatewayError
from app.core.logging import get_logger, request_id_var, setup_logging
from app.core.middleware import RequestIdMiddleware, RequestLoggingMiddleware
from app.schemas.common import ErrorDetail, ErrorResponse

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown."""
    settings = get_settings()
    setup_logging(settings.log_level)
    logger.info(
        f"Starting AI Gateway v{settings.service_version} "
        f"with provider={settings.ai_provider}, model={settings.ai_model}"
    )
    yield
    logger.info("Shutting down AI Gateway")


app = FastAPI(
    title="AI Gateway",
    description="Unified API Gateway for AI Providers",
    version=get_settings().service_version,
    lifespan=lifespan,
)

# Add middleware (order matters: first added = outermost)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIdMiddleware)

# Register routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(analyze_router)


@app.exception_handler(GatewayError)
async def gateway_error_handler(request: Request, exc: GatewayError) -> JSONResponse:
    """Handle custom gateway exceptions."""
    request_id = request_id_var.get() or "unknown"

    error_response = ErrorResponse(
        error=ErrorDetail(
            code=exc.code.value,
            message=exc.message,
            request_id=request_id,
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    request_id = request_id_var.get() or "unknown"
    logger.exception(f"Unexpected error: {exc}")

    error_response = ErrorResponse(
        error=ErrorDetail(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            request_id=request_id,
        )
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(),
    )
