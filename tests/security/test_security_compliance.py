"""
Security validation tests for AUDITORIA360
Tests for hardcoded credentials removal and SQL injection prevention
"""

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock

from src.core.secrets import SecretsManager
from src.core.validation import InputValidator


class TestSecretsManager:
    """Test secure secrets management"""
    
    def test_no_hardcoded_credentials_in_migration(self):
        """Verify no hardcoded credentials in migration file"""
        with open("migrations/001_enhanced_auth_migration.py", "r") as f:
            content = f.read()
        
        # Check that hardcoded passwords are not present
        assert "senha_admin" not in content
        assert "senha_gestor_a" not in content
        assert "senha_gestor_b" not in content
        assert "senha_cliente_x" not in content
        
        # Verify it uses secrets manager
        assert "secrets_manager" in content
        assert "get_default_passwords" in content
    
    def test_no_hardcoded_credentials_in_auth(self):
        """Verify no hardcoded credentials in auth file"""
        with open("src/auth/unified_auth.py", "r") as f:
            content = f.read()
        
        # Check that hardcoded passwords are not present
        assert "senha_admin" not in content
        assert "senha_gestor_a" not in content
        assert "senha_gestor_b" not in content
        assert "senha_cliente_x" not in content
        
        # Verify it uses secure secrets manager
        assert "from src.core.secrets import secrets_manager" in content
        assert "secrets_manager.get_secret_key()" in content
    
    @patch.dict(os.environ, {
        'ENVIRONMENT': 'development',
        'DEFAULT_ADMIN_PASSWORD': 'test_secure_admin_123!',
        'DEFAULT_GESTOR_A_PASSWORD': 'test_secure_gestor_a_123!',
        'DEFAULT_GESTOR_B_PASSWORD': 'test_secure_gestor_b_123!',
        'DEFAULT_CLIENT_X_PASSWORD': 'test_secure_client_x_123!'
    })
    def test_secrets_manager_uses_env_vars(self):
        """Test that secrets manager uses environment variables"""
        manager = SecretsManager()
        passwords = manager.get_default_passwords()
        
        assert passwords["admin"] == "test_secure_admin_123!"
        assert passwords["gestor_a"] == "test_secure_gestor_a_123!"
        assert passwords["gestor_b"] == "test_secure_gestor_b_123!"
        assert passwords["client_x"] == "test_secure_client_x_123!"
    
    @patch.dict(os.environ, {'ENVIRONMENT': 'production'}, clear=True)
    def test_production_requires_secure_passwords(self):
        """Test that production environment requires secure passwords"""
        manager = SecretsManager()
        
        with pytest.raises(ValueError, match="Production environment requires secure"):
            manager.get_default_passwords()
    
    def test_secure_password_generation(self):
        """Test that generated passwords are secure"""
        manager = SecretsManager()
        password = manager.generate_secure_password(16)
        
        assert len(password) == 16
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in "!@#$%^&*" for c in password)
    
    def test_secret_key_validation(self):
        """Test that secret key validation works"""
        # Test with short key in production
        with patch.dict(os.environ, {'SECRET_KEY': 'a' * 31, 'ENVIRONMENT': 'production'}, clear=True):
            manager = SecretsManager()
            with pytest.raises(ValueError, match="SECRET_KEY must be at least 32 characters in production"):
                manager.get_secret_key()


class TestInputValidation:
    """Test input validation and SQL injection prevention"""
    
    def test_sql_identifier_validation(self):
        """Test SQL identifier validation"""
        # Valid identifiers
        assert InputValidator.validate_sql_identifier("table_name")
        assert InputValidator.validate_sql_identifier("column_123")
        assert InputValidator.validate_sql_identifier("valid-name")
        
        # Invalid identifiers
        assert not InputValidator.validate_sql_identifier("table'; DROP TABLE users; --")
        assert not InputValidator.validate_sql_identifier("column with spaces")
        assert not InputValidator.validate_sql_identifier("column@domain.com")
        assert not InputValidator.validate_sql_identifier("")
        assert not InputValidator.validate_sql_identifier("a" * 101)  # Too long
    
    def test_sql_injection_prevention(self):
        """Test SQL injection pattern detection"""
        # Safe inputs
        safe_input = "John Doe"
        assert InputValidator.sanitize_sql_input(safe_input) == "John Doe"
        
        # Test specific dangerous inputs
        with pytest.raises(ValueError, match="potentially dangerous SQL patterns"):
            InputValidator.sanitize_sql_input("'; DROP TABLE users; --")
        
        with pytest.raises(ValueError, match="potentially dangerous SQL patterns"):
            InputValidator.sanitize_sql_input("1 OR 1=1")
        
        with pytest.raises(ValueError, match="potentially dangerous SQL patterns"):
            InputValidator.sanitize_sql_input("UNION SELECT * FROM passwords")
    
    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Safe HTML
        safe_html = "<b>Bold text</b>"
        result = InputValidator.sanitize_html_input(safe_html, ['b'])
        assert result == "<b>Bold text</b>"
        
        # Dangerous scripts should be removed
        dangerous_inputs = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "<iframe src='javascript:alert(1)'></iframe>",
            "<a href='javascript:alert(1)'>Click me</a>",
        ]
        
        for dangerous_input in dangerous_inputs:
            result = InputValidator.sanitize_html_input(dangerous_input)
            assert "<script" not in result.lower()
            assert "javascript:" not in result.lower()
            assert "onerror" not in result.lower()
    
    def test_user_input_sanitization(self):
        """Test comprehensive user input sanitization"""
        input_data = {
            "username": "test_user",
            "email": "test@example.com", 
            "comment": "<script>alert('xss')</script>Normal text",
            "id": 123,
            "nested": {
                "field": "'; DROP TABLE users; --"
            }
        }
        
        sanitized = InputValidator.sanitize_user_input(input_data)
        
        assert sanitized["username"] == "test_user"
        assert sanitized["email"] == "test@example.com"
        assert "script" not in sanitized["comment"].lower()
        assert sanitized["id"] == 123
        # Dangerous nested field should be skipped or sanitized
        assert "nested" not in sanitized or "DROP TABLE" not in str(sanitized.get("nested", ""))
    
    def test_email_validation(self):
        """Test email validation"""
        # Valid emails
        assert InputValidator.validate_email("test@example.com")
        assert InputValidator.validate_email("user.name+tag@domain.co.uk")
        
        # Invalid emails
        assert not InputValidator.validate_email("invalid-email")
        assert not InputValidator.validate_email("@domain.com")
        assert not InputValidator.validate_email("user@")
        assert not InputValidator.validate_email("")


class TestSecurityCompliance:
    """Test overall security compliance"""
    
    def test_no_database_credentials_in_code(self):
        """Verify no database credentials are hardcoded"""
        # Check migration file
        with open("migrations/001_enhanced_auth_migration.py", "r") as f:
            content = f.read()
        
        # Should not contain default database URL with credentials
        # The fallback class is acceptable as it's just a fallback with placeholders
        lines_with_postgres = [line for line in content.split('\n') if 'postgresql://user:password@localhost' in line]
        # Allow only in the fallback class definition, not in actual usage
        assert all('return os.getenv' in line or 'SimpleSecretsManager' in content[content.find(line)-200:content.find(line)] for line in lines_with_postgres), \
            "Database credentials should only appear in fallback implementations"
        assert "secrets_manager.get_database_url()" in content
    
    def test_sql_queries_use_parameterization(self):
        """Verify SQL queries use parameterization"""
        # Check ML training utils
        with open("scripts/ml_training/utils.py", "r") as f:
            content = f.read()
        
        # Should not use f-strings for SQL
        assert "f\"SELECT * FROM" not in content
        assert "_validate_sql_identifier" in content
        assert "table_ref = client.dataset" in content
    
    def test_bq_loader_uses_safe_queries(self):
        """Verify BigQuery loader uses safe query construction"""
        with open("services/ingestion/bq_loader.py", "r") as f:
            content = f.read()
        
        # Should validate column names
        assert "ALLOWED_UPDATE_COLUMNS" in content
        assert "InputValidator.validate_sql_identifier" in content
    
    def test_environment_template_updated(self):
        """Verify environment template includes security variables"""
        with open(".env.template", "r") as f:
            content = f.read()
        
        assert "DEFAULT_ADMIN_PASSWORD" in content
        assert "SECRET_KEY" in content
        assert "AWS_SECRETS_MANAGER" in content or "SECRET_MANAGER" in content
        assert "changeme" in content  # Should show placeholder passwords


if __name__ == "__main__":
    pytest.main([__file__])