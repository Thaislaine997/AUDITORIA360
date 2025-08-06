
"""
Legacy API Deprecation Middleware
Added by API Unification Protocol
"""

from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LegacyAPIDeprecationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add deprecation warnings to legacy API endpoints
    """
    
    def __init__(self, app, sunset_date: str = "2025-11-04T18:47:01.899697"):
        super().__init__(app)
        self.sunset_date = sunset_date
        
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add deprecation headers to all responses
        response.headers["X-API-Deprecated"] = "true"
        response.headers["X-API-Sunset-Date"] = self.sunset_date
        response.headers["X-API-Migration-Guide"] = "/docs/api-migration"
        response.headers["Deprecation"] = self.sunset_date
        
        # Log deprecation usage
        logger.warning(f"DEPRECATED API USAGE: {request.method} {request.url.path} from {request.client.host}")
        
        return response
