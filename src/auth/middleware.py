"""
Enhanced Authorization Middleware for Multi-Level Access Control
Implements secure data scoping and permission checking for AUDITORIA360
"""

from functools import wraps
from typing import Any, Dict, List, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .unified_auth import UnifiedAuthManager

# Initialize auth manager and security
auth_manager = UnifiedAuthManager()
security = HTTPBearer(auto_error=False)


class AuthorizationMiddleware:
    """Enhanced middleware for multi-level authorization and data scoping"""

    def __init__(self):
        self.auth_manager = auth_manager

    async def get_current_user(
        self, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> Dict[str, Any]:
        """Get current authenticated user with enhanced profile data"""
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = self.auth_manager.verify_token(credentials.credentials)
            user_data = payload.get("user_data", {})
            
            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token",
                )

            # Add computed access scope
            user_data["access_scope"] = self.auth_manager.get_user_data_scope(user_data)
            return user_data

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def require_permission(self, required_permission: str):
        """Decorator to require specific permission"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Get current user from kwargs or dependency injection
                current_user = kwargs.get("current_user")
                if not current_user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )

                if not self.auth_manager.check_permission(current_user, required_permission):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permission '{required_permission}' required"
                    )

                return await func(*args, **kwargs)
            return wrapper
        return decorator

    def require_user_type(self, allowed_types: List[str]):
        """Decorator to require specific user types"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                current_user = kwargs.get("current_user")
                if not current_user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )

                user_type = current_user.get("user_type", "")
                if user_type not in allowed_types:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access restricted to: {', '.join(allowed_types)}"
                    )

                return await func(*args, **kwargs)
            return wrapper
        return decorator

    def scope_data_access(self, resource_type: str):
        """Decorator to automatically scope data access based on user permissions"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                current_user = kwargs.get("current_user")
                if not current_user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )

                # Add data scope filters to kwargs
                scope = current_user.get("access_scope", {})
                if scope.get("scope_type") != "all":
                    kwargs["data_filters"] = scope.get("filters", {})
                    kwargs["scope_type"] = scope.get("scope_type")

                return await func(*args, **kwargs)
            return wrapper
        return decorator

    async def authorize_resource_access(
        self, 
        current_user: Dict[str, Any], 
        resource_type: str, 
        resource_id: str = None
    ) -> bool:
        """Authorize user access to specific resource"""
        return self.auth_manager.authorize_data_access(current_user, resource_type, resource_id)


# Global middleware instance
auth_middleware = AuthorizationMiddleware()

# Dependency functions for FastAPI
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """FastAPI dependency to get current user"""
    return await auth_middleware.get_current_user(credentials)

async def get_super_admin_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """FastAPI dependency for super admin only endpoints"""
    if current_user.get("user_type") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user

async def get_contabilidade_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """FastAPI dependency for contabilidade level access"""
    allowed_types = ["super_admin", "contabilidade"]
    if current_user.get("user_type") not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contabilidade or admin access required"
        )
    return current_user

async def get_any_authenticated_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """FastAPI dependency for any authenticated user"""
    return current_user


# Decorator shortcuts
require_super_admin = auth_middleware.require_user_type(["super_admin"])
require_contabilidade = auth_middleware.require_user_type(["super_admin", "contabilidade"])
require_any_auth = auth_middleware.require_user_type(["super_admin", "contabilidade", "cliente_final"])

# Permission decorators
require_full_access = auth_middleware.require_permission("full_access")
require_company_access = auth_middleware.require_permission("view_company_data")
require_own_data_access = auth_middleware.require_permission("view_own_data")

# Data scoping decorators
scope_company_data = auth_middleware.scope_data_access("company")
scope_enterprise_data = auth_middleware.scope_data_access("enterprise")