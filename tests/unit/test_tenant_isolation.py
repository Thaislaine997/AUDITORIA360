"""
Tests for Multi-Tenant Isolation Middleware
Validates tenant data isolation and cross-tenant access prevention
"""

from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.core.tenant_middleware import (
    TenantIsolationMiddleware,
    TenantScope,
    get_tenant_aware_query_filter,
    require_tenant_access,
    validate_cross_tenant_access,
)


class TestTenantScope:
    """Test TenantScope functionality"""

    def test_admin_can_access_any_tenant(self):
        """Test that admin users can access any tenant"""
        admin_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="administrador"
        )

        assert admin_scope.can_access_tenant("empresa1")
        assert admin_scope.can_access_tenant("empresa2")
        assert admin_scope.can_access_tenant("empresa999")

    def test_regular_user_can_only_access_own_tenant(self):
        """Test that regular users can only access their own tenant"""
        user_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="colaborador"
        )

        assert user_scope.can_access_tenant("empresa1")
        assert not user_scope.can_access_tenant("empresa2")
        assert not user_scope.can_access_tenant("empresa999")

    def test_data_filter_clause_for_admin(self):
        """Test data filter generation for admin users"""
        admin_scope = TenantScope(tenant_id="empresa1", user_role="administrador")

        filter_clause = admin_scope.get_data_filter_clause()
        assert filter_clause == "1=1"  # Admin sees all data

        filter_clause_with_alias = admin_scope.get_data_filter_clause("e")
        assert filter_clause_with_alias == "1=1"

    def test_data_filter_clause_for_regular_user(self):
        """Test data filter generation for regular users"""
        user_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="colaborador"
        )

        filter_clause = user_scope.get_data_filter_clause()
        assert filter_clause == "empresa_id = 'empresa1'"

        filter_clause_with_alias = user_scope.get_data_filter_clause("e")
        assert filter_clause_with_alias == "e.empresa_id = 'empresa1'"


class TestTenantIsolationMiddleware:
    """Test TenantIsolationMiddleware functionality"""

    def test_extract_tenant_from_user_with_empresa_id(self):
        """Test tenant extraction when user has empresa_id"""
        middleware = TenantIsolationMiddleware()

        user_data = {
            "empresa_id": "empresa123",
            "role": "contador",
            "permissions": ["read:payroll", "write:payroll"],
        }

        tenant_scope = middleware.extract_tenant_from_user(user_data)

        assert tenant_scope.tenant_id == "empresa123"
        assert tenant_scope.empresa_id == "empresa123"
        assert tenant_scope.user_role == "contador"
        assert "read:payroll" in tenant_scope.permissions

    def test_extract_tenant_from_user_with_defaults(self):
        """Test tenant extraction with default values"""
        middleware = TenantIsolationMiddleware()

        user_data = {"user_id": "user123"}

        tenant_scope = middleware.extract_tenant_from_user(user_data)

        assert tenant_scope.tenant_id == "default"
        assert tenant_scope.empresa_id == "default"
        assert tenant_scope.user_role == "colaborador"
        assert len(tenant_scope.permissions) == 0

    @patch("src.core.tenant_middleware.logger")
    def test_apply_rls_filter_for_regular_user(self, mock_logger):
        """Test RLS filter application for regular users"""
        middleware = TenantIsolationMiddleware()
        mock_db = Mock(spec=Session)

        tenant_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="colaborador"
        )

        middleware.apply_rls_filter(mock_db, tenant_scope)

        # Verify that execute was called with the RLS filter
        mock_db.execute.assert_called_once()
        call_args = mock_db.execute.call_args

        # Check that we have the SQL text and parameters
        text_clause = call_args.args[0]
        params = call_args.args[1]

        assert "SET LOCAL app.current_empresa_id" in str(text_clause)
        assert params["empresa_id"] == "empresa1"

    def test_apply_rls_filter_for_admin(self):
        """Test RLS filter application for admin users (should be skipped)"""
        middleware = TenantIsolationMiddleware()
        mock_db = Mock(spec=Session)

        admin_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="administrador"
        )

        middleware.apply_rls_filter(mock_db, admin_scope)

        # Admin users should not have RLS filters applied
        mock_db.execute.assert_not_called()

    def test_validate_tenant_access_same_tenant(self):
        """Test validation when accessing same tenant data"""
        middleware = TenantIsolationMiddleware()

        tenant_scope = TenantScope(
            tenant_id="empresa1",
            empresa_id="empresa1",
            user_role="colaborador",
            permissions=["read:data"],
        )

        requested_data = {"empresa_id": "empresa1", "resource_type": "data"}

        result = middleware.validate_tenant_access(tenant_scope, requested_data)
        assert result is True

    def test_validate_tenant_access_cross_tenant_denied(self):
        """Test validation when attempting cross-tenant access"""
        middleware = TenantIsolationMiddleware()

        tenant_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="colaborador"
        )

        requested_data = {"empresa_id": "empresa2", "resource_type": "data"}

        result = middleware.validate_tenant_access(tenant_scope, requested_data)
        assert result is False

    def test_validate_tenant_access_admin_cross_tenant_allowed(self):
        """Test validation for admin cross-tenant access"""
        middleware = TenantIsolationMiddleware()

        admin_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="administrador"
        )

        requested_data = {"empresa_id": "empresa2", "resource_type": "data"}

        result = middleware.validate_tenant_access(admin_scope, requested_data)
        assert result is True


class TestHelperFunctions:
    """Test helper functions for tenant isolation"""

    def test_get_tenant_aware_query_filter_regular_user(self):
        """Test query filter generation for regular users"""
        tenant_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="colaborador"
        )

        filter_clause = get_tenant_aware_query_filter("employees", tenant_scope)
        assert filter_clause == "employees.empresa_id = 'empresa1'"

    def test_get_tenant_aware_query_filter_admin(self):
        """Test query filter generation for admin users"""
        admin_scope = TenantScope(tenant_id="empresa1", user_role="administrador")

        filter_clause = get_tenant_aware_query_filter("employees", admin_scope)
        assert filter_clause == "1=1"

    def test_validate_cross_tenant_access_allowed(self):
        """Test cross-tenant access validation - allowed case"""
        user_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="colaborador"
        )

        result = validate_cross_tenant_access(user_scope, "empresa1")
        assert result is True

    def test_validate_cross_tenant_access_denied(self):
        """Test cross-tenant access validation - denied case"""
        user_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="colaborador"
        )

        result = validate_cross_tenant_access(user_scope, "empresa2")
        assert result is False

    def test_validate_cross_tenant_access_admin_allowed(self):
        """Test cross-tenant access validation - admin allowed"""
        admin_scope = TenantScope(
            tenant_id="empresa1", empresa_id="empresa1", user_role="administrador"
        )

        result = validate_cross_tenant_access(admin_scope, "empresa2")
        assert result is True


@pytest.fixture
def mock_user_data():
    """Fixture providing mock user data"""
    return {
        "user_id": "user123",
        "empresa_id": "empresa1",
        "role": "colaborador",
        "permissions": ["read:payroll", "read:documents"],
    }


class TestTenantAccessDecorator:
    """Test the require_tenant_access decorator"""

    @pytest.mark.asyncio
    async def test_require_tenant_access_with_valid_user(self, mock_user_data):
        """Test decorator with valid user data"""

        @require_tenant_access(operation="read", resource_type="payroll")
        def protected_function(user_data=None, tenant_scope=None):
            return {"status": "success", "tenant": tenant_scope.empresa_id}

        result = protected_function(user_data=mock_user_data)

        assert result["status"] == "success"
        assert result["tenant"] == "empresa1"

    def test_require_tenant_access_without_user_raises_error(self):
        """Test decorator without user data raises authentication error"""

        @require_tenant_access(operation="read", resource_type="payroll")
        def protected_function():
            return {"status": "success"}

        with pytest.raises(HTTPException) as exc_info:
            protected_function()

        assert exc_info.value.status_code == 401
        assert "Authentication required" in str(exc_info.value.detail)
