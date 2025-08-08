"""
Unit tests for src.core.security module.
"""

import os
from datetime import timedelta
from unittest.mock import patch

import pytest

from src.core.exceptions import AuthenticationError
from src.core.security import SecurityManager, security_manager


class TestSecurityManager:
    """Test cases for SecurityManager class."""

    def test_init_with_default_values(self):
        """Test SecurityManager initialization with default values."""
        with patch.dict(os.environ, {}, clear=True):
            manager = SecurityManager()

            assert manager.secret_key == "your-secret-key-here-change-in-production"
            assert manager.algorithm == "HS256"
            assert manager.access_token_expire_minutes == 30

    def test_init_with_environment_variables(self):
        """Test SecurityManager initialization with environment variables."""
        with patch.dict(
            os.environ,
            {"SECRET_KEY": "test-secret-key", "ACCESS_TOKEN_EXPIRE_MINUTES": "60"},
        ):
            manager = SecurityManager()

            assert manager.secret_key == "test-secret-key"
            assert manager.access_token_expire_minutes == 60

    def test_get_password_hash(self):
        """Test password hashing."""
        manager = SecurityManager()
        password = "test_password"

        hashed = manager.get_password_hash(password)

        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        manager = SecurityManager()
        password = "test_password"

        hashed = manager.get_password_hash(password)
        result = manager.verify_password(password, hashed)

        assert result is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        manager = SecurityManager()
        password = "test_password"
        wrong_password = "wrong_password"

        hashed = manager.get_password_hash(password)
        result = manager.verify_password(wrong_password, hashed)

        assert result is False

    def test_create_access_token_default_expiry(self):
        """Test creating access token with default expiry."""
        manager = SecurityManager()
        data = {"sub": "testuser", "role": "user"}

        token = manager.create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_custom_expiry(self):
        """Test creating access token with custom expiry."""
        manager = SecurityManager()
        data = {"sub": "testuser", "role": "user"}
        custom_expiry = timedelta(minutes=60)

        token = manager.create_access_token(data, expires_delta=custom_expiry)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid(self):
        """Test verifying a valid token."""
        manager = SecurityManager()
        data = {"sub": "testuser", "role": "user"}

        token = manager.create_access_token(data)
        payload = manager.verify_token(token)

        assert payload["sub"] == "testuser"
        assert payload["role"] == "user"
        assert "exp" in payload

    def test_verify_token_invalid(self):
        """Test verifying an invalid token."""
        manager = SecurityManager()
        invalid_token = "invalid.token.here"

        with pytest.raises(AuthenticationError, match="Invalid token"):
            manager.verify_token(invalid_token)

    def test_verify_token_expired(self):
        """Test verifying an expired token."""
        manager = SecurityManager()
        data = {"sub": "testuser", "role": "user"}

        # Create token with past expiry
        past_expiry = timedelta(minutes=-1)
        token = manager.create_access_token(data, expires_delta=past_expiry)

        with pytest.raises(AuthenticationError, match="Invalid token"):
            manager.verify_token(token)

    def test_verify_token_tampered(self):
        """Test verifying a tampered token."""
        manager = SecurityManager()
        data = {"sub": "testuser", "role": "user"}

        token = manager.create_access_token(data)
        # Tamper with the token
        tampered_token = token[:-5] + "xxxxx"

        with pytest.raises(AuthenticationError, match="Invalid token"):
            manager.verify_token(tampered_token)


class TestGlobalSecurityManager:
    """Test cases for global security_manager instance."""

    def test_global_instance_exists(self):
        """Test that global security_manager instance exists."""
        assert security_manager is not None
        assert isinstance(security_manager, SecurityManager)

    def test_global_instance_methods(self):
        """Test that global security_manager has required methods."""
        assert hasattr(security_manager, "verify_password")
        assert hasattr(security_manager, "get_password_hash")
        assert hasattr(security_manager, "create_access_token")
        assert hasattr(security_manager, "verify_token")

    def test_password_integration(self):
        """Test password hashing and verification integration."""
        password = "integration_test_password"

        hashed = security_manager.get_password_hash(password)
        verified = security_manager.verify_password(password, hashed)

        assert verified is True

    def test_token_integration(self):
        """Test token creation and verification integration."""
        data = {"sub": "integration_user", "permissions": ["read", "write"]}

        token = security_manager.create_access_token(data)
        payload = security_manager.verify_token(token)

        assert payload["sub"] == "integration_user"
        assert payload["permissions"] == ["read", "write"]
