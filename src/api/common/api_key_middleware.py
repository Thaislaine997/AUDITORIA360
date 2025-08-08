"""
API Key Middleware - Security and Rate Limiting for Public API

This middleware implements comprehensive API key authentication and rate limiting
for the AUDITORIA360 public API, enabling the API-as-a-Product strategy.

Part of Initiative III: Partnership Ecosystem Activation
"""

import logging
import time
from collections import defaultdict
from datetime import datetime
from functools import wraps
from typing import Any, Dict, Optional, Tuple

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    In-memory rate limiter for API requests
    In production, this should be backed by Redis for scalability
    """

    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 300  # Clean up old entries every 5 minutes
        self.last_cleanup = time.time()

    def is_allowed(
        self, key: str, limit: int = 1000, window: int = 3600
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if request is allowed based on rate limit

        Args:
            key: Unique identifier (usually API key)
            limit: Maximum requests allowed in window
            window: Time window in seconds (default: 1 hour)

        Returns:
            Tuple of (is_allowed, metadata)
        """
        current_time = time.time()

        # Cleanup old entries periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries(current_time - window)
            self.last_cleanup = current_time

        # Get request timestamps for this key
        timestamps = self.requests[key]

        # Remove expired timestamps
        timestamps[:] = [ts for ts in timestamps if current_time - ts < window]

        # Check if limit is exceeded
        if len(timestamps) >= limit:
            # Find when the oldest request will expire
            oldest_request = min(timestamps)
            reset_time = oldest_request + window

            return False, {
                "limit": limit,
                "remaining": 0,
                "reset": int(reset_time),
                "retry_after": int(reset_time - current_time),
            }

        # Add current request
        timestamps.append(current_time)

        return True, {
            "limit": limit,
            "remaining": limit - len(timestamps),
            "reset": int(current_time + window),
            "retry_after": 0,
        }

    def _cleanup_old_entries(self, cutoff_time: float):
        """Remove entries older than cutoff_time"""
        for key in list(self.requests.keys()):
            self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff_time]
            if not self.requests[key]:
                del self.requests[key]


class APIKeyManager:
    """
    Manages API key validation and permissions
    In production, this would be backed by a database
    """

    def __init__(self):
        # Mock API keys for demonstration
        # In production, these would be stored in database with proper encryption
        self.api_keys = {
            "ak_prod_1234567890abcdef": {
                "name": "Produção Principal",
                "user_id": 1001,
                "permissions": ["read:employees", "read:payroll", "write:reports"],
                "status": "active",
                "created_at": "2024-01-15",
                "rate_limit": 1000,  # requests per hour
                "usage_count": 15420,
            },
            "ak_dev_abcdef1234567890": {
                "name": "Desenvolvimento",
                "user_id": 1002,
                "permissions": ["read:employees", "read:payroll"],
                "status": "active",
                "created_at": "2024-01-10",
                "rate_limit": 500,
                "usage_count": 2340,
            },
            "ak_partner_fedcba0987654321": {
                "name": "Parceiro Integração",
                "user_id": 2001,
                "permissions": ["read:employees", "read:reports"],
                "status": "active",
                "created_at": "2024-01-05",
                "rate_limit": 2000,
                "usage_count": 8950,
            },
        }

    def validate_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Validate API key and return key metadata

        Args:
            api_key: The API key to validate

        Returns:
            API key metadata if valid, None if invalid
        """
        if not api_key or not api_key.startswith("ak_"):
            return None

        key_data = self.api_keys.get(api_key)
        if not key_data or key_data["status"] != "active":
            return None

        return key_data

    def has_permission(self, api_key: str, required_permission: str) -> bool:
        """
        Check if API key has required permission

        Args:
            api_key: The API key
            required_permission: Required permission (e.g., "read:employees")

        Returns:
            True if permission is granted
        """
        key_data = self.validate_key(api_key)
        if not key_data:
            return False

        permissions = key_data.get("permissions", [])

        # Check for admin permission
        if "admin:all" in permissions:
            return True

        # Check for specific permission
        if required_permission in permissions:
            return True

        # Check for wildcard permissions (e.g., "read:*")
        permission_parts = required_permission.split(":")
        if len(permission_parts) == 2:
            wildcard_permission = f"{permission_parts[0]}:*"
            if wildcard_permission in permissions:
                return True

        return False

    def increment_usage(self, api_key: str):
        """Increment usage counter for API key"""
        if api_key in self.api_keys:
            self.api_keys[api_key]["usage_count"] += 1

    def get_rate_limit(self, api_key: str) -> int:
        """Get rate limit for API key"""
        key_data = self.validate_key(api_key)
        return key_data.get("rate_limit", 100) if key_data else 100


# Global instances
rate_limiter = RateLimiter()
api_key_manager = APIKeyManager()
security = HTTPBearer()


def log_api_request(
    api_key: str, request: Request, response_time: float, status_code: int
):
    """
    Log API request for monitoring and analytics
    In production, this would write to a structured logging system or database
    """
    key_data = api_key_manager.validate_key(api_key)
    user_id = key_data.get("user_id", "unknown") if key_data else "unknown"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "api_key": api_key[:8] + "...",  # Truncate for security
        "user_id": user_id,
        "method": request.method,
        "endpoint": str(request.url.path),
        "query_params": dict(request.query_params),
        "user_agent": request.headers.get("user-agent", ""),
        "ip_address": request.client.host if request.client else "unknown",
        "response_time_ms": round(response_time * 1000, 2),
        "status_code": status_code,
    }

    logger.info(f"API Request: {log_entry}")


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = security,
) -> Dict[str, Any]:
    """
    FastAPI dependency to verify API key authentication

    Returns:
        API key metadata

    Raises:
        HTTPException: If API key is invalid
    """
    api_key = credentials.credentials

    # Validate API key
    key_data = api_key_manager.validate_key(api_key)
    if not key_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "api_key": api_key,
        "user_id": key_data["user_id"],
        "permissions": key_data["permissions"],
        "rate_limit": key_data["rate_limit"],
    }


def require_permission(permission: str):
    """
    Decorator to require specific permission for endpoint access

    Args:
        permission: Required permission (e.g., "read:employees")
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract API key from function arguments
            api_key_data = None
            for arg in args:
                if isinstance(arg, dict) and "api_key" in arg:
                    api_key_data = arg
                    break

            if not api_key_data:
                # Look in kwargs
                api_key_data = kwargs.get("api_key_data")

            if not api_key_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required"
                )

            # Check permission
            if not api_key_manager.has_permission(api_key_data["api_key"], permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{permission}' required",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


class APIKeyMiddleware:
    """
    FastAPI middleware class for API key authentication and rate limiting
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        # Skip middleware for non-API endpoints
        if not request.url.path.startswith("/api/v1/public/"):
            await self.app(scope, receive, send)
            return

        start_time = time.time()

        try:
            # Extract API key from Authorization header
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                await self._send_error(send, 401, "Authorization header required")
                return

            api_key = auth_header[7:]  # Remove "Bearer " prefix

            # Validate API key
            key_data = api_key_manager.validate_key(api_key)
            if not key_data:
                await self._send_error(send, 401, "Invalid API key")
                return

            # Check rate limit
            rate_limit = key_data.get("rate_limit", 1000)
            is_allowed, rate_info = rate_limiter.is_allowed(api_key, rate_limit)

            if not is_allowed:
                await self._send_rate_limit_error(send, rate_info)
                return

            # Add API key data to request state
            scope["api_key_data"] = {
                "api_key": api_key,
                "user_id": key_data["user_id"],
                "permissions": key_data["permissions"],
            }

            # Create response wrapper to capture status code
            response_status = [200]

            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    response_status[0] = message["status"]
                    # Add rate limit headers
                    headers = list(message.get("headers", []))
                    headers.extend(
                        [
                            (b"x-ratelimit-limit", str(rate_info["limit"]).encode()),
                            (
                                b"x-ratelimit-remaining",
                                str(rate_info["remaining"]).encode(),
                            ),
                            (b"x-ratelimit-reset", str(rate_info["reset"]).encode()),
                        ]
                    )
                    message["headers"] = headers
                await send(message)

            # Process request
            await self.app(scope, receive, send_wrapper)

            # Log request
            response_time = time.time() - start_time
            api_key_manager.increment_usage(api_key)
            log_api_request(api_key, request, response_time, response_status[0])

        except Exception as e:
            logger.error(f"API Key Middleware error: {e}")
            await self._send_error(send, 500, "Internal server error")

    async def _send_error(self, send, status_code: int, message: str):
        """Send error response"""
        await send(
            {
                "type": "http.response.start",
                "status": status_code,
                "headers": [
                    (b"content-type", b"application/json"),
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": f'{{"error": "{message}"}}'.encode(),
            }
        )

    async def _send_rate_limit_error(self, send, rate_info: Dict[str, Any]):
        """Send rate limit exceeded response"""
        await send(
            {
                "type": "http.response.start",
                "status": 429,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"x-ratelimit-limit", str(rate_info["limit"]).encode()),
                    (b"x-ratelimit-remaining", str(rate_info["remaining"]).encode()),
                    (b"x-ratelimit-reset", str(rate_info["reset"]).encode()),
                    (b"retry-after", str(rate_info["retry_after"]).encode()),
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": f'{{"error": "Rate limit exceeded", "retry_after": {rate_info["retry_after"]}}}'.encode(),
            }
        )


# Utility functions for FastAPI integration


def get_api_key_data(request: Request) -> Optional[Dict[str, Any]]:
    """
    Extract API key data from request scope

    Args:
        request: FastAPI Request object

    Returns:
        API key data if available
    """
    return getattr(request, "scope", {}).get("api_key_data")


def require_api_permission(permission: str):
    """
    FastAPI dependency to require specific API permission

    Usage:
        @app.get("/api/v1/public/employees", dependencies=[require_api_permission("read:employees")])
        async def get_employees(...):
            ...
    """

    async def dependency(request: Request):
        api_key_data = get_api_key_data(request)
        if not api_key_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API authentication required",
            )

        api_key = api_key_data["api_key"]
        if not api_key_manager.has_permission(api_key, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required",
            )

        return api_key_data

    return dependency


# Usage example:
"""
from fastapi import FastAPI, Depends
from src.api.common.api_key_middleware import APIKeyMiddleware, require_api_permission

app = FastAPI()

# Add middleware
app.add_middleware(APIKeyMiddleware)

# Protected endpoint
@app.get("/api/v1/public/employees")
async def get_employees(api_key_data = Depends(require_api_permission("read:employees"))):
    # api_key_data contains validated API key information
    user_id = api_key_data["user_id"]
    # ... endpoint logic
    return {"employees": []}
"""
