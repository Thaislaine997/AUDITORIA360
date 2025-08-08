"""
Middleware for standardized error handling and logging across the AUDITORIA360 API
"""

import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .responses import ErrorCode, create_error_response

logger = logging.getLogger(__name__)


class StandardizedErrorMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle errors consistently across all endpoints
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID for tracking
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Log request start
        start_time = time.time()
        logger.info(
            f"Request started: {request.method} {request.url}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "user_agent": request.headers.get("user-agent", "unknown"),
            },
        )

        try:
            response = await call_next(request)

            # Log successful response
            process_time = time.time() - start_time
            logger.info(
                f"Request completed: {request.method} {request.url} - {response.status_code}",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "process_time": process_time,
                },
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as exc:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url} - {type(exc).__name__}: {str(exc)}",
                extra={
                    "request_id": request_id,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "process_time": process_time,
                },
                exc_info=True,
            )

            # Create standardized error response
            error_response = create_error_response(
                error_code=ErrorCode.INTERNAL_SERVER_ERROR,
                message="An unexpected error occurred",
                trace_id=request_id,
                request_id=request_id,
            )

            return JSONResponse(
                status_code=500,
                content=error_response.dict(),
                headers={"X-Request-ID": request_id},
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for detailed request/response logging
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Log request details
        logger.debug(
            f"Request details: {request.method} {request.url}",
            extra={
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
                "path_params": dict(request.path_params),
            },
        )

        response = await call_next(request)

        # Log response details
        logger.debug(
            f"Response details: {response.status_code}",
            extra={
                "response_headers": dict(response.headers),
                "status_code": response.status_code,
            },
        )

        return response


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware for monitoring API performance
    """

    def __init__(self, app, slow_request_threshold: float = 1.0):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        # Log slow requests
        if process_time > self.slow_request_threshold:
            logger.warning(
                f"Slow request detected: {request.method} {request.url} took {process_time:.3f}s",
                extra={
                    "request_id": getattr(request.state, "request_id", "unknown"),
                    "process_time": process_time,
                    "threshold": self.slow_request_threshold,
                },
            )

        # Add performance headers
        response.headers["X-Process-Time"] = str(process_time)

        return response
