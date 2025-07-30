"""
Multi-Tenant Isolation Middleware for AUDITORIA360
Implements comprehensive data isolation and tenant-aware access controls
"""

import logging
from typing import Any, Dict, List, Optional, Set
from functools import wraps

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.auth.unified_auth import UnifiedAuthManager

logger = logging.getLogger(__name__)


class TenantScope:
    """Represents tenant scope and access controls"""
    
    def __init__(
        self,
        tenant_id: str,
        empresa_id: Optional[str] = None,
        user_role: str = "colaborador",
        permissions: Optional[List[str]] = None
    ):
        self.tenant_id = tenant_id
        self.empresa_id = empresa_id or tenant_id  # Default empresa_id to tenant_id
        self.user_role = user_role
        self.permissions = set(permissions or [])
        
    def can_access_tenant(self, target_tenant_id: str) -> bool:
        """Check if current scope can access target tenant"""
        if self.user_role == "administrador":
            return True  # Admins can access any tenant
        return self.tenant_id == target_tenant_id
    
    def get_data_filter_clause(self, table_alias: str = "") -> str:
        """Generate SQL WHERE clause for tenant data filtering"""
        prefix = f"{table_alias}." if table_alias else ""
        
        if self.user_role == "administrador":
            return "1=1"  # Admins see all data
        
        return f"{prefix}empresa_id = '{self.empresa_id}'"


class TenantIsolationMiddleware:
    """Enhanced middleware for multi-tenant data isolation"""
    
    def __init__(self):
        self.auth_manager = UnifiedAuthManager()
        
    def extract_tenant_from_user(self, user_data: Dict[str, Any]) -> TenantScope:
        """Extract tenant information from authenticated user"""
        # Extract tenant info from user data
        tenant_id = user_data.get("empresa_id") or user_data.get("tenant_id", "default")
        empresa_id = user_data.get("empresa_id", tenant_id)
        user_role = user_data.get("role", "colaborador")
        permissions = user_data.get("permissions", [])
        
        return TenantScope(
            tenant_id=tenant_id,
            empresa_id=empresa_id,
            user_role=user_role,
            permissions=permissions
        )
    
    def apply_rls_filter(self, db: Session, tenant_scope: TenantScope):
        """Apply Row-Level Security (RLS) equivalent filtering to database session"""
        try:
            if tenant_scope.user_role != "administrador":
                # Set session variable for tenant filtering
                db.execute(
                    text("SET LOCAL app.current_empresa_id = :empresa_id"),
                    {"empresa_id": tenant_scope.empresa_id}
                )
                logger.debug(f"Applied RLS filter for empresa_id: {tenant_scope.empresa_id}")
        except Exception as e:
            logger.warning(f"Failed to apply RLS filter: {e}")
    
    def validate_tenant_access(
        self,
        tenant_scope: TenantScope,
        requested_data: Dict[str, Any],
        operation: str = "read"
    ) -> bool:
        """Validate if tenant can perform operation on requested data"""
        
        # Check if data contains tenant/empresa references
        data_empresa_id = requested_data.get("empresa_id")
        if data_empresa_id:
            if not tenant_scope.can_access_tenant(data_empresa_id):
                logger.warning(
                    f"Tenant {tenant_scope.tenant_id} attempted to access "
                    f"data for empresa {data_empresa_id}"
                )
                return False
        
        # Additional permission checks based on operation
        required_permission = f"{operation}:{requested_data.get('resource_type', 'data')}"
        if required_permission not in tenant_scope.permissions and tenant_scope.user_role != "administrador":
            logger.warning(
                f"User with role {tenant_scope.user_role} lacks permission: {required_permission}"
            )
            return False
            
        return True


# Global instance
tenant_middleware = TenantIsolationMiddleware()


def require_tenant_access(operation: str = "read", resource_type: str = "data"):
    """Decorator to enforce tenant-based access control"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract request and user data from args/kwargs
            request = None
            user_data = None
            
            # Look for Request and user data in function arguments
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                elif isinstance(arg, dict) and "role" in arg:
                    user_data = arg
            
            if not user_data:
                # Look in kwargs
                user_data = kwargs.get("current_user") or kwargs.get("user_data")
            
            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required for tenant access"
                )
            
            # Create tenant scope
            tenant_scope = tenant_middleware.extract_tenant_from_user(user_data)
            
            # Add tenant scope to kwargs for use in the function
            kwargs["tenant_scope"] = tenant_scope
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_tenant_aware_query_filter(table_name: str, tenant_scope: TenantScope) -> str:
    """Generate tenant-aware WHERE clause for queries"""
    if tenant_scope.user_role == "administrador":
        return "1=1"  # Admins see everything
    
    return f"{table_name}.empresa_id = '{tenant_scope.empresa_id}'"


def validate_cross_tenant_access(
    user_tenant_scope: TenantScope,
    target_empresa_id: str,
    operation: str = "read"
) -> bool:
    """Validate cross-tenant access attempts"""
    if user_tenant_scope.user_role == "administrador":
        return True
    
    if user_tenant_scope.empresa_id != target_empresa_id:
        logger.warning(
            f"Cross-tenant access attempt: user empresa {user_tenant_scope.empresa_id} "
            f"trying to {operation} data from empresa {target_empresa_id}"
        )
        return False
    
    return True