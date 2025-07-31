"""
Tests for unified authentication system
"""

from datetime import timedelta
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from src.auth.unified_auth import UnifiedAuthManager, auth_manager


def test_unified_auth_manager_creation():
    """Test UnifiedAuthManager can be instantiated"""
    auth = UnifiedAuthManager()
    assert auth is not None
    assert hasattr(auth, "hash_password")
    assert hasattr(auth, "verify_password")
    assert hasattr(auth, "create_access_token")


def test_global_auth_manager():
    """Test global auth_manager instance exists"""
    assert auth_manager is not None
    assert isinstance(auth_manager, UnifiedAuthManager)


def test_password_hashing():
    """Test password hashing and verification"""
    auth = UnifiedAuthManager()

    password = "test_password_123"
    hashed = auth.hash_password(password)

    assert hashed != password
    assert len(hashed) > 20
    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("wrong_password", hashed)


def test_access_token_creation():
    """Test JWT access token creation"""
    auth = UnifiedAuthManager()

    data = {"sub": "testuser", "roles": ["user"]}
    token = auth.create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 50
    assert token.count(".") == 2  # JWT format


def test_access_token_with_expiry():
    """Test JWT token creation with custom expiry"""
    auth = UnifiedAuthManager()

    data = {"sub": "testuser"}
    custom_expiry = timedelta(minutes=30)
    token = auth.create_access_token(data, expires_delta=custom_expiry)

    # Should be a valid JWT token
    assert isinstance(token, str)
    assert len(token) > 50


def test_token_verification():
    """Test JWT token verification"""
    auth = UnifiedAuthManager()

    data = {"sub": "testuser", "roles": ["user"]}
    token = auth.create_access_token(data)

    payload = auth.verify_token(token)
    assert payload["sub"] == "testuser"
    assert "exp" in payload
    assert "iat" in payload


def test_token_verification_invalid():
    """Test JWT token verification with invalid token"""
    auth = UnifiedAuthManager()

    with pytest.raises(HTTPException) as exc_info:
        auth.verify_token("invalid_token")

    assert exc_info.value.status_code == 401


@patch("src.auth.unified_auth.Path")
def test_yaml_config_loading(mock_path):
    """Test YAML configuration loading"""
    # Mock file doesn't exist
    mock_path.return_value.exists.return_value = False

    auth = UnifiedAuthManager()

    # Should have default config
    assert "credentials" in auth.yaml_config
    assert "usernames" in auth.yaml_config["credentials"]


def test_yaml_authentication():
    """Test authentication against YAML configuration"""
    auth = UnifiedAuthManager()

    # Should have default admin user
    result = auth._authenticate_yaml_user("admin", "admin123")
    assert result is True

    # Wrong password
    result = auth._authenticate_yaml_user("admin", "wrong_password")
    assert result is False

    # Non-existent user
    result = auth._authenticate_yaml_user("nonexistent", "password")
    assert result is False


def test_user_authentication():
    """Test full user authentication"""
    auth = UnifiedAuthManager()

    # Valid user
    user = auth.authenticate_user("admin", "admin123")
    assert user is not None
    assert user["username"] == "admin"
    assert "email" in user
    assert "roles" in user

    # Invalid user
    user = auth.authenticate_user("admin", "wrong_password")
    assert user is None


def test_login_success():
    """Test successful login"""
    auth = UnifiedAuthManager()

    result = auth.login("admin", "admin123")

    assert "access_token" in result
    assert "token_type" in result
    assert result["token_type"] == "bearer"
    assert "expires_in" in result
    assert "user" in result
    assert result["user"]["username"] == "admin"


def test_login_failure():
    """Test failed login"""
    auth = UnifiedAuthManager()

    with pytest.raises(HTTPException) as exc_info:
        auth.login("admin", "wrong_password")

    assert exc_info.value.status_code == 401
    assert "Incorrect username or password" in str(exc_info.value.detail)


def test_get_current_user_from_token():
    """Test getting current user from token"""
    auth = UnifiedAuthManager()

    # Create token
    login_result = auth.login("admin", "admin123")
    token = login_result["access_token"]

    # Get user from token
    user = auth.get_current_user_from_token(token)

    assert user is not None
    assert user["username"] == "admin"
    assert "email" in user
    assert "roles" in user


def test_get_current_user_from_invalid_token():
    """Test getting current user from invalid token"""
    auth = UnifiedAuthManager()

    user = auth.get_current_user_from_token("invalid_token")
    assert user is None

    user = auth.get_current_user_from_token(None)
    assert user is None


def test_logout():
    """Test logout functionality"""
    auth = UnifiedAuthManager()

    result = auth.logout()
    assert result["message"] == "Successfully logged out"
    assert result["status"] == "success"

def test_convenience_functions():
    """Test convenience functions"""
    from src.auth.unified_auth import (
        authenticate_user,
        create_access_token,
        hash_password,
        verify_password,
    )

    # Test they exist and are callable
    assert callable(hash_password)
    assert callable(verify_password)
    assert callable(create_access_token)
    assert callable(authenticate_user)

    # Test basic functionality
    password = "test123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)

    token = create_access_token({"sub": "test"})
    assert isinstance(token, str)

    user = authenticate_user("admin", "admin123")
    assert user is not None
