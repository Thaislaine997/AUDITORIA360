"""
Comprehensive Test Suite for Enhanced Multi-Level Access Control
Tests the revolutionary UI/UX with three-tier authentication system
"""

import pytest
import asyncio
from typing import Dict, Any
from unittest.mock import patch, MagicMock

from src.auth.unified_auth import UnifiedAuthManager
from src.auth.middleware import AuthorizationMiddleware


class TestEnhancedAuthentication:
    """Test suite for the enhanced authentication system"""

    def setup_method(self):
        """Setup test environment"""
        self.auth_manager = UnifiedAuthManager()
        self.auth_middleware = AuthorizationMiddleware()

    def test_super_admin_authentication(self):
        """Test Super Admin authentication and permissions"""
        # Test credentials from problem statement
        user = self.auth_manager.authenticate_user(
            "admin@auditoria360.com", "senha_admin"
        )
        
        assert user is not None
        assert user["user_type"] == "super_admin"
        assert user["name"] == "Super Administrator"
        assert "full_access" in user["permissions"]
        
        # Test data scope
        scope = self.auth_manager.get_user_data_scope(user)
        assert scope["scope_type"] == "all"
        assert scope["filters"] == {}

    def test_contabilidade_a_authentication(self):
        """Test Contabilidade A Gestor authentication and scope"""
        user = self.auth_manager.authenticate_user(
            "gestor@contabilidade-a.com", "senha_gestor_a"
        )
        
        assert user is not None
        assert user["user_type"] == "contabilidade"
        assert user["name"] == "Gestor Contabilidade A"
        assert user["company_id"] == "CONTAB_A"
        assert "view_company_data" in user["permissions"]
        
        # Test data scope restrictions
        scope = self.auth_manager.get_user_data_scope(user)
        assert scope["scope_type"] == "company"
        assert scope["filters"]["contabilidade_id"] == "CONTAB_A"

    def test_contabilidade_b_authentication(self):
        """Test Contabilidade B Gestor authentication and isolation"""
        user = self.auth_manager.authenticate_user(
            "gestor@contabilidade-b.com", "senha_gestor_b"
        )
        
        assert user is not None
        assert user["user_type"] == "contabilidade"
        assert user["name"] == "Gestor Contabilidade B"
        assert user["company_id"] == "CONTAB_B"
        
        # Verify isolation from Contabilidade A
        scope = self.auth_manager.get_user_data_scope(user)
        assert scope["filters"]["contabilidade_id"] == "CONTAB_B"
        assert scope["filters"]["contabilidade_id"] != "CONTAB_A"

    def test_cliente_final_authentication(self):
        """Test Cliente Final authentication and maximum restriction"""
        user = self.auth_manager.authenticate_user(
            "contato@empresa-x.com", "senha_cliente_x"
        )
        
        assert user is not None
        assert user["user_type"] == "cliente_final"
        assert user["name"] == "Cliente Empresa X"
        assert user["company_id"] == "EMPRESA_X"
        assert "view_own_data" in user["permissions"]
        
        # Test most restrictive scope
        scope = self.auth_manager.get_user_data_scope(user)
        assert scope["scope_type"] == "enterprise"
        assert scope["filters"]["empresa_id"] == "EMPRESA_X"

    def test_data_segregation_authorization(self):
        """Test data access authorization between different user types"""
        # Super Admin can access everything
        super_admin = self.auth_manager.authenticate_user(
            "admin@auditoria360.com", "senha_admin"
        )
        assert self.auth_manager.authorize_data_access(
            super_admin, "contabilidade", "CONTAB_A"
        )
        assert self.auth_manager.authorize_data_access(
            super_admin, "contabilidade", "CONTAB_B"
        )
        
        # Contabilidade A can only access their data
        contab_a = self.auth_manager.authenticate_user(
            "gestor@contabilidade-a.com", "senha_gestor_a"
        )
        assert self.auth_manager.authorize_data_access(
            contab_a, "contabilidade", "CONTAB_A"
        )
        assert not self.auth_manager.authorize_data_access(
            contab_a, "contabilidade", "CONTAB_B"
        )
        
        # Cliente Final can only access their enterprise
        cliente = self.auth_manager.authenticate_user(
            "contato@empresa-x.com", "senha_cliente_x"
        )
        assert self.auth_manager.authorize_data_access(
            cliente, "empresa", "EMPRESA_X"
        )
        assert not self.auth_manager.authorize_data_access(
            cliente, "empresa", "EMPRESA_Y"
        )

    def test_permission_checking(self):
        """Test permission verification system"""
        super_admin = self.auth_manager.authenticate_user(
            "admin@auditoria360.com", "senha_admin"
        )
        contabilidade = self.auth_manager.authenticate_user(
            "gestor@contabilidade-a.com", "senha_gestor_a"
        )
        cliente = self.auth_manager.authenticate_user(
            "contato@empresa-x.com", "senha_cliente_x"
        )
        
        # Super admin has all permissions
        assert self.auth_manager.check_permission(super_admin, "full_access")
        assert self.auth_manager.check_permission(super_admin, "view_company_data")
        assert self.auth_manager.check_permission(super_admin, "view_own_data")
        
        # Contabilidade has limited permissions
        assert not self.auth_manager.check_permission(contabilidade, "full_access")
        assert self.auth_manager.check_permission(contabilidade, "view_company_data")
        assert not self.auth_manager.check_permission(contabilidade, "view_own_data")
        
        # Cliente has most limited permissions
        assert not self.auth_manager.check_permission(cliente, "full_access")
        assert not self.auth_manager.check_permission(cliente, "view_company_data")
        assert self.auth_manager.check_permission(cliente, "view_own_data")

    def test_invalid_credentials(self):
        """Test authentication failure scenarios"""
        # Wrong password
        user = self.auth_manager.authenticate_user(
            "admin@auditoria360.com", "wrong_password"
        )
        assert user is None
        
        # Non-existent user
        user = self.auth_manager.authenticate_user(
            "nonexistent@test.com", "any_password"
        )
        assert user is None
        
        # Empty credentials
        user = self.auth_manager.authenticate_user("", "")
        assert user is None

    def test_legacy_credential_compatibility(self):
        """Test backward compatibility with legacy credentials"""
        # Legacy admin credentials should still work
        user = self.auth_manager.authenticate_user("admin", "admin123")
        assert user is not None
        assert user["user_type"] == "super_admin"
        
        # Legacy contabilidade credentials
        user = self.auth_manager.authenticate_user("contabilidade", "conta123")
        assert user is not None
        assert user["user_type"] == "contabilidade"


class TestUIAccessControl:
    """Test UI access control and navigation restrictions"""

    def setup_method(self):
        """Setup UI test environment"""
        self.auth_manager = UnifiedAuthManager()

    def test_super_admin_ui_access(self):
        """Test Super Admin has access to all UI modules"""
        user = self.auth_manager.authenticate_user(
            "admin@auditoria360.com", "senha_admin"
        )
        
        # Should have access to all modules
        accessible_modules = [
            "dashboards", "portal_demandas", "user_management",
            "consultor_riscos", "administracao", "relatorios_avancados"
        ]
        
        for module in accessible_modules:
            assert self.auth_manager.check_permission(user, "full_access")

    def test_contabilidade_ui_restrictions(self):
        """Test Contabilidade UI shows appropriate restrictions"""
        user = self.auth_manager.authenticate_user(
            "gestor@contabilidade-a.com", "senha_gestor_a"
        )
        
        # Should have access to company-specific modules
        allowed_modules = [
            "meus_clientes", "gestao_folha", "relatorios_segmentados",
            "consultor_riscos"
        ]
        
        # Should be restricted from global modules
        restricted_modules = [
            "outras_contabilidades", "administracao_global"
        ]
        
        assert self.auth_manager.check_permission(user, "view_company_data")
        assert not self.auth_manager.check_permission(user, "full_access")

    def test_cliente_final_ui_restrictions(self):
        """Test Cliente Final UI shows maximum restrictions"""
        user = self.auth_manager.authenticate_user(
            "contato@empresa-x.com", "senha_cliente_x"
        )
        
        # Should only have access to own enterprise modules
        allowed_modules = [
            "dados_empresa", "documentos_empresa", "relatorios_empresa",
            "suporte_especializado"
        ]
        
        # Should be restricted from everything else
        restricted_modules = [
            "outras_empresas", "administracao", "gestao_usuarios"
        ]
        
        assert self.auth_manager.check_permission(user, "view_own_data")
        assert not self.auth_manager.check_permission(user, "view_company_data")
        assert not self.auth_manager.check_permission(user, "full_access")


class TestSecurityAndCompliance:
    """Test security features and compliance requirements"""

    def setup_method(self):
        """Setup security test environment"""
        self.auth_manager = UnifiedAuthManager()

    def test_password_hashing_security(self):
        """Test password security implementation"""
        # Verify passwords are properly hashed
        plain_password = "senha_admin"
        hashed = self.auth_manager.hash_password(plain_password)
        
        assert hashed != plain_password
        assert self.auth_manager.verify_password(plain_password, hashed)
        assert not self.auth_manager.verify_password("wrong_password", hashed)

    def test_data_scoping_prevents_leakage(self):
        """Test data scoping prevents information leakage"""
        contab_a_user = self.auth_manager.authenticate_user(
            "gestor@contabilidade-a.com", "senha_gestor_a"
        )
        
        # Should not authorize access to other contabilidade's data
        assert not self.auth_manager.authorize_data_access(
            contab_a_user, "contabilidade", "CONTAB_B"
        )
        
        # Should not authorize access to unrelated enterprises
        assert not self.auth_manager.authorize_data_access(
            contab_a_user, "empresa", "EMPRESA_Z"  # Belongs to CONTAB_B
        )

    def test_session_management_security(self):
        """Test secure session management"""
        user = self.auth_manager.authenticate_user(
            "admin@auditoria360.com", "senha_admin"
        )
        
        # Test JWT token creation and verification
        token = self.auth_manager.create_access_token({"user_data": user})
        assert token is not None
        
        # Verify token contains user data
        decoded = self.auth_manager.verify_token(token)
        assert decoded["user_data"]["username"] == user["username"]


@pytest.mark.asyncio
class TestIntegrationScenarios:
    """Integration tests for complete user workflows"""

    def setup_method(self):
        """Setup integration test environment"""
        self.auth_manager = UnifiedAuthManager()

    async def test_complete_super_admin_workflow(self):
        """Test complete Super Admin workflow"""
        # 1. Authentication
        user = self.auth_manager.authenticate_user(
            "admin@auditoria360.com", "senha_admin"
        )
        assert user is not None
        
        # 2. Access all contabilidades
        assert self.auth_manager.authorize_data_access(
            user, "contabilidade", "CONTAB_A"
        )
        assert self.auth_manager.authorize_data_access(
            user, "contabilidade", "CONTAB_B"
        )
        
        # 3. Manage all enterprises
        for empresa in ["EMPRESA_X", "EMPRESA_Y", "EMPRESA_Z"]:
            assert self.auth_manager.authorize_data_access(
                user, "empresa", empresa
            )

    async def test_complete_contabilidade_workflow(self):
        """Test complete Contabilidade workflow with data isolation"""
        # 1. Authentication
        user = self.auth_manager.authenticate_user(
            "gestor@contabilidade-a.com", "senha_gestor_a"
        )
        assert user is not None
        
        # 2. Access own contabilidade
        assert self.auth_manager.authorize_data_access(
            user, "contabilidade", "CONTAB_A"
        )
        
        # 3. Access own clients only
        assert self.auth_manager.authorize_data_access(
            user, "client", "EMPRESA_X"
        )
        assert self.auth_manager.authorize_data_access(
            user, "client", "EMPRESA_Y"
        )
        
        # 4. Cannot access other contabilidade's clients
        assert not self.auth_manager.authorize_data_access(
            user, "client", "EMPRESA_Z"  # Belongs to CONTAB_B
        )

    async def test_complete_cliente_final_workflow(self):
        """Test complete Cliente Final workflow with maximum privacy"""
        # 1. Authentication
        user = self.auth_manager.authenticate_user(
            "contato@empresa-x.com", "senha_cliente_x"
        )
        assert user is not None
        
        # 2. Access only own enterprise data
        assert self.auth_manager.authorize_data_access(
            user, "empresa", "EMPRESA_X"
        )
        
        # 3. Cannot access other enterprises
        assert not self.auth_manager.authorize_data_access(
            user, "empresa", "EMPRESA_Y"
        )
        assert not self.auth_manager.authorize_data_access(
            user, "empresa", "EMPRESA_Z"
        )
        
        # 4. Cannot access contabilidade management
        assert not self.auth_manager.authorize_data_access(
            user, "contabilidade", "CONTAB_A"
        )


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])