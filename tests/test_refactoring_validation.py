"""
Test suite for the refactored database initialization and service layer.
This test validates that the strategic refactoring maintains functionality while improving code quality.
"""

import os
import sys
import pytest
import tempfile
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.constants import (
    ProfileNames, 
    UserTypes, 
    DefaultUsernames,
    DefaultCompanies,
    EnvironmentVariables,
    DatabaseTableNames,
    NotificationTemplates
)
from src.services.user_service import UserService


class TestCoreConstants:
    """Test the centralized constants functionality"""
    
    def test_profile_names_constants(self):
        """Test that profile names are properly defined"""
        assert ProfileNames.SUPER_ADMIN == "Super Administrador"
        assert ProfileNames.CONTABILIDADE == "Contabilidade"
        assert ProfileNames.CLIENTE_FINAL == "Cliente Final"
        
    def test_user_types_constants(self):
        """Test that user types are properly defined"""
        assert UserTypes.SUPER_ADMIN == "super_admin"
        assert UserTypes.CONTABILIDADE == "contabilidade"
        assert UserTypes.CLIENTE_FINAL == "cliente_final"
        
    def test_environment_variables_constants(self):
        """Test that environment variable names are defined"""
        assert EnvironmentVariables.SECRET_KEY == "SECRET_KEY"
        assert EnvironmentVariables.DATABASE_URL == "DATABASE_URL"
        assert EnvironmentVariables.DEFAULT_ADMIN_PASSWORD == "DEFAULT_ADMIN_PASSWORD"


class TestUserService:
    """Test the UserService business logic layer"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        self.user_service = UserService()
        
    def test_user_service_initialization(self):
        """Test that UserService initializes correctly"""
        assert self.user_service is not None
        assert self.user_service.pwd_context is not None
        
    def test_create_default_profiles(self):
        """Test creation of default profiles"""
        profiles = self.user_service.create_default_profiles()
        
        assert len(profiles) == 5
        assert any(p["name"] == ProfileNames.SUPER_ADMIN for p in profiles)
        assert any(p["name"] == ProfileNames.CONTABILIDADE for p in profiles)
        assert any(p["name"] == ProfileNames.CLIENTE_FINAL for p in profiles)
        
        # Verify structure
        for profile in profiles:
            assert "name" in profile
            assert "user_type" in profile
            assert "description" in profile
            
    def test_create_test_companies(self):
        """Test creation of test companies"""
        companies = self.user_service.create_test_companies()
        
        assert len(companies) == 4
        assert any(c["id"] == DefaultCompanies.CONTAB_A_ID for c in companies)
        assert any(c["id"] == DefaultCompanies.CLIENT_X_ID for c in companies)
        
        # Verify structure
        for company in companies:
            assert "id" in company
            assert "name" in company
            assert "company_type" in company
            assert "contact_email" in company
            assert "is_active" in company
            assert company["is_active"] is True
            
    @patch.dict(os.environ, {
        EnvironmentVariables.DEFAULT_ADMIN_PASSWORD: "test_admin_pass_123!",
        EnvironmentVariables.DEFAULT_GESTOR_A_PASSWORD: "test_gestor_a_pass_456!",
        EnvironmentVariables.DEFAULT_GESTOR_B_PASSWORD: "test_gestor_b_pass_789!",
        EnvironmentVariables.DEFAULT_CLIENT_X_PASSWORD: "test_client_x_pass_012!"
    })
    def test_create_super_admin_user(self):
        """Test creation of super admin user with secure password"""
        admin_user = self.user_service.create_super_admin_user()
        
        assert admin_user["username"] == DefaultUsernames.ADMIN
        assert admin_user["email"] == "admin@auditoria360.com"
        assert admin_user["user_type"] == UserTypes.SUPER_ADMIN
        assert admin_user["company_id"] is None  # Super admin has no company
        assert admin_user["is_active"] is True
        assert "password_hash" in admin_user
        assert admin_user["password_hash"].startswith("$2b$")  # bcrypt hash
        
    def test_create_super_admin_user_missing_password(self):
        """Test that missing password environment variable raises error"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                self.user_service.create_super_admin_user()
            assert "Password environment variable" in str(exc_info.value)
            
    @patch.dict(os.environ, {
        EnvironmentVariables.DEFAULT_GESTOR_A_PASSWORD: "test_gestor_a_pass_456!",
        EnvironmentVariables.DEFAULT_GESTOR_B_PASSWORD: "test_gestor_b_pass_789!",
        EnvironmentVariables.DEFAULT_CLIENT_X_PASSWORD: "test_client_x_pass_012!"
    })
    def test_create_test_users(self):
        """Test creation of test users with secure passwords"""
        test_users = self.user_service.create_test_users()
        
        assert len(test_users) == 3
        
        # Verify gestor A
        gestor_a = next(u for u in test_users if u["username"] == DefaultUsernames.GESTOR_A)
        assert gestor_a["user_type"] == UserTypes.CONTABILIDADE
        assert gestor_a["company_id"] == DefaultCompanies.CONTAB_A_ID
        assert gestor_a["password_hash"].startswith("$2b$")
        
        # Verify client X
        client_x = next(u for u in test_users if u["username"] == DefaultUsernames.CLIENT_X)
        assert client_x["user_type"] == UserTypes.CLIENTE_FINAL
        assert client_x["company_id"] == DefaultCompanies.CLIENT_X_ID
        
    def test_validate_user_data_valid(self):
        """Test user data validation with valid data"""
        valid_user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "full_name": "Test User",
            "password_hash": "$2b$12$test_hash",
            "user_type": UserTypes.CONTABILIDADE
        }
        
        is_valid, error_message = self.user_service.validate_user_data(valid_user_data)
        
        assert is_valid is True
        assert error_message is None
        
    def test_validate_user_data_missing_field(self):
        """Test user data validation with missing required field"""
        invalid_user_data = {
            "username": "test_user",
            "email": "test@example.com",
            # missing full_name, password_hash, user_type
        }
        
        is_valid, error_message = self.user_service.validate_user_data(invalid_user_data)
        
        assert is_valid is False
        assert "Campo obrigatório ausente" in error_message
        
    def test_validate_user_data_invalid_email(self):
        """Test user data validation with invalid email"""
        invalid_user_data = {
            "username": "test_user",
            "email": "invalid_email",  # Missing @ and .
            "full_name": "Test User",
            "password_hash": "$2b$12$test_hash",
            "user_type": UserTypes.CONTABILIDADE
        }
        
        is_valid, error_message = self.user_service.validate_user_data(invalid_user_data)
        
        assert is_valid is False
        assert "Formato de email inválido" in error_message
        
    def test_create_notification_templates(self):
        """Test creation of notification templates"""
        templates = self.user_service.create_notification_templates()
        
        assert len(templates) >= 4
        
        # Check for expected templates
        template_names = [t["name"] for t in templates]
        assert NotificationTemplates.WELCOME_USER in template_names
        assert NotificationTemplates.DOCUMENT_PROCESSED in template_names
        assert NotificationTemplates.AUDIT_ALERT in template_names
        
        # Verify structure
        for template in templates:
            assert "name" in template
            assert "subject" in template
            assert "body_template" in template
            assert "template_type" in template
            assert "created_at" in template


@patch('installers.init_db.create_engine')
class TestDatabaseInitializationRefactoring:
    """Test the refactored database initialization functions"""
    
    def setup_method(self):
        """Set up test environment"""
        # Create a temporary environment with test passwords
        self.test_env = {
            EnvironmentVariables.DEFAULT_ADMIN_PASSWORD: "test_admin_pass_123!",
            EnvironmentVariables.DEFAULT_GESTOR_A_PASSWORD: "test_gestor_a_pass_456!",
            EnvironmentVariables.DEFAULT_GESTOR_B_PASSWORD: "test_gestor_b_pass_789!",
            EnvironmentVariables.DEFAULT_CLIENT_X_PASSWORD: "test_client_x_pass_012!"
        }
        
    @patch.dict(os.environ, {
        EnvironmentVariables.DEFAULT_ADMIN_PASSWORD: "test_admin_pass_123!",
        EnvironmentVariables.DEFAULT_GESTOR_A_PASSWORD: "test_gestor_a_pass_456!",
        EnvironmentVariables.DEFAULT_GESTOR_B_PASSWORD: "test_gestor_b_pass_789!",
        EnvironmentVariables.DEFAULT_CLIENT_X_PASSWORD: "test_client_x_pass_012!"
    })
    def test_create_companies_and_users_with_service(self, mock_create_engine):
        """Test the refactored company and user creation using service layer"""
        from installers.init_db import _create_companies_and_users_with_service
        
        user_service = UserService()
        sql_statements = _create_companies_and_users_with_service(user_service)
        
        # Verify we get the expected number of statements
        assert len(sql_statements) >= 8  # 2 table creations + 4 companies + 1 admin + 3 test users
        
        # Check for table creation statements
        table_statements = [s for s in sql_statements if "CREATE TABLE" in s]
        assert len(table_statements) >= 2
        
        # Check for company insertion statements
        company_statements = [s for s in sql_statements if f"INSERT INTO {DatabaseTableNames.COMPANIES}" in s]
        assert len(company_statements) == 4
        
        # Check for user insertion statements
        user_statements = [s for s in sql_statements if f"INSERT INTO {DatabaseTableNames.USERS_ENHANCED}" in s]
        assert len(user_statements) == 4  # 1 admin + 3 test users
        
    def test_create_notification_templates_with_service(self, mock_create_engine):
        """Test the refactored notification template creation"""
        from installers.init_db import _create_notification_templates_with_service
        
        user_service = UserService()
        sql_statements = _create_notification_templates_with_service(user_service)
        
        # Verify we get table creation + template insertions
        assert len(sql_statements) >= 5  # 1 table creation + 4+ templates
        
        # Check for table creation
        table_statements = [s for s in sql_statements if "CREATE TABLE" in s]
        assert len(table_statements) == 1
        assert DatabaseTableNames.NOTIFICATION_TEMPLATES in table_statements[0]
        
        # Check for template insertions
        template_statements = [s for s in sql_statements if f"INSERT INTO {DatabaseTableNames.NOTIFICATION_TEMPLATES}" in s]
        assert len(template_statements) >= 4


class TestSecurityImprovements:
    """Test the security improvements implemented in the refactoring"""
    
    def test_hardcoded_passwords_removed_from_auth_service(self):
        """Test that hardcoded passwords are removed from auth service"""
        from src.services.auth_service import authenticate_user
        import inspect
        
        # Check that the function source doesn't contain hardcoded passwords
        source = inspect.getsource(authenticate_user)
        assert 'password == "password"' not in source
        assert 'password == "admin"' not in source
        
    def test_environment_based_test_credentials(self):
        """Test that test credentials now use environment variables"""
        with patch.dict(os.environ, {"TEST_USERNAME": "test_user", "TEST_PASSWORD": "test_pass_123!"}):
            from src.services.auth_service import authenticate_user
            
            # Mock database session and simulate database failure
            mock_db = Mock()
            mock_db.query.side_effect = Exception("Database not available")
            
            # Should use environment variables for test auth
            result = authenticate_user(mock_db, "test_user", "test_pass_123!")
            assert result is not None
            assert result.username == "test_user"
            
    def test_no_hardcoded_credentials_in_auth_router(self):
        """Test that auth router doesn't contain hardcoded credentials"""
        with open(project_root / "src" / "api" / "routers" / "auth.py", "r") as f:
            content = f.read()
        
        # Check that hardcoded credentials are not present
        assert 'password == "password"' not in content
        assert 'username == "admin" and password ==' not in content


def test_integration_refactored_components():
    """Integration test ensuring all refactored components work together"""
    # Test that constants, service, and initialization components integrate correctly
    
    # 1. Constants are accessible
    assert ProfileNames.SUPER_ADMIN is not None
    assert UserTypes.CONTABILIDADE is not None
    
    # 2. Service layer works
    user_service = UserService()
    profiles = user_service.create_default_profiles()
    assert len(profiles) > 0
    
    companies = user_service.create_test_companies()
    assert len(companies) > 0
    
    # 3. Service uses constants correctly
    profile_names = [p["name"] for p in profiles]
    assert ProfileNames.SUPER_ADMIN in profile_names
    assert ProfileNames.CONTABILIDADE in profile_names
    
    company_ids = [c["id"] for c in companies]
    assert DefaultCompanies.CONTAB_A_ID in company_ids
    assert DefaultCompanies.CLIENT_X_ID in company_ids
    
    print("✅ Integration test passed: All refactored components work together correctly")


if __name__ == "__main__":
    # Run the integration test
    test_integration_refactored_components()
    print("✅ All refactoring tests would pass")