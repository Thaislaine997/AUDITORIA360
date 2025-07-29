"""
Tests for authentication service functions
"""
import pytest
from unittest.mock import Mock, patch
from src.services.auth_service import (
    hash_password, verify_password, create_access_token,
    authenticate_user, get_current_user, create_user, 
    get_users, get_user_by_id, update_user
)

def test_hash_password():
    """Test password hashing function"""
    password = "test_password"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 20  # BCrypt hashes are long
    assert hashed.startswith("$2b$")  # BCrypt prefix

def test_verify_password():
    """Test password verification"""
    password = "test_password"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "test_user"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 50  # JWT tokens are long
    assert token.count(".") == 2  # JWT has 3 parts separated by dots

def test_authenticate_user_with_mock_db():
    """Test user authentication with mock database"""
    mock_db = Mock()
    
    # Test successful authentication
    user = authenticate_user(mock_db, "admin", "password")
    assert user is not None
    assert user.username == "admin"
    
    # Test failed authentication
    user = authenticate_user(mock_db, "invalid", "invalid")
    assert user is None

def test_get_current_user_mock():
    """Test get current user function"""
    with patch('src.services.auth_service.security') as mock_security, \
         patch('src.services.auth_service.get_db') as mock_get_db:
        
        # Mock dependencies
        mock_credentials = Mock()
        mock_credentials.credentials = "mock_token"
        mock_db = Mock()
        
        # Test the mock functionality
        user = get_current_user()
        assert user is not None
        assert hasattr(user, 'username')

def test_create_user_functionality():
    """Test create user function"""
    from src.schemas.auth_schemas import UserCreate
    from unittest.mock import Mock
    
    mock_db = Mock()
    user_data = Mock()
    user_data.username = "new_user"
    user_data.email = "new_user@example.com"
    user_data.password = "password"
    
    user = create_user(mock_db, user_data)
    assert user is not None
    assert user.username == "new_user"

def test_get_users_functionality():
    """Test get users function"""
    mock_db = Mock()
    
    users = get_users(mock_db)
    assert isinstance(users, list)
    assert len(users) > 0
    assert all(hasattr(user, 'username') for user in users)

def test_get_user_by_id_functionality():
    """Test get user by ID function"""
    mock_db = Mock()
    
    user = get_user_by_id(mock_db, 1)
    assert user is not None
    assert user.id == 1
    assert hasattr(user, 'username')

def test_update_user_functionality():
    """Test update user function"""
    from unittest.mock import Mock
    
    mock_db = Mock()
    user_data = Mock()
    
    user = update_user(mock_db, 1, user_data)
    assert user is not None
    assert user.id == 1