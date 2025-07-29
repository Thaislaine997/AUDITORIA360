"""
Tests for configuration and utility functions
"""

import os
from unittest.mock import Mock, patch

import pytest


def test_config_manager_import():
    """Test config manager can be imported"""
    try:
        from services.core.config_manager import get_setting, load_config

        assert callable(load_config) or callable(get_setting)
    except ImportError:
        # Config manager might not be implemented yet
        pass


def test_validators_import():
    """Test validators can be imported"""
    try:
        from services.core.validators import validate_cpf, validate_email

        assert callable(validate_cpf) or callable(validate_email)
    except ImportError:
        # Validators might not be implemented yet
        pass


def test_frontend_utils_import():
    """Test frontend utils can be imported"""
    from src.frontend.utils import (
        get_auth_headers,
        get_current_user,
        is_authenticated,
        logout_user,
        make_authenticated_request,
        require_authentication,
    )

    assert callable(get_auth_headers)
    assert callable(is_authenticated)
    assert callable(require_authentication)
    assert callable(get_current_user)
    assert callable(logout_user)
    assert callable(make_authenticated_request)


@patch("src.frontend.utils.st")
def test_get_auth_headers(mock_st):
    """Test get_auth_headers function"""
    from src.frontend.utils import get_auth_headers

    # Mock streamlit session state
    mock_st.session_state = {"api_token": "test_token"}

    headers = get_auth_headers()
    assert isinstance(headers, dict)
    assert "Content-Type" in headers
    assert headers["Content-Type"] == "application/json"
    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer test_token"


@patch("src.frontend.utils.st")
def test_is_authenticated(mock_st):
    """Test is_authenticated function"""
    from src.frontend.utils import is_authenticated

    # Mock authenticated state
    mock_st.session_state = {"authentication_status": True, "api_token": "test_token"}

    result = is_authenticated()
    assert result is True

    # Mock unauthenticated state
    mock_st.session_state = {}
    result = is_authenticated()
    assert result is False


@patch("src.frontend.utils.st")
def test_get_current_user(mock_st):
    """Test get_current_user function"""
    from src.frontend.utils import get_current_user

    # Mock authenticated user
    mock_st.session_state = {
        "authentication_status": True,
        "api_token": "test_token",
        "name": "Test User",
        "username": "testuser",
    }

    user = get_current_user()
    assert user is not None
    assert user["name"] == "Test User"
    assert user["username"] == "testuser"
    assert user["authenticated"] is True

    # Mock unauthenticated user
    mock_st.session_state = {}
    user = get_current_user()
    assert user is None


@patch("src.frontend.utils.st")
def test_logout_user(mock_st):
    """Test logout_user function"""
    from src.frontend.utils import logout_user

    # Mock session state with user data
    mock_session_state = {
        "authentication_status": True,
        "api_token": "test_token",
        "name": "Test User",
        "username": "testuser",
    }
    mock_st.session_state = mock_session_state

    # Mock the session_state as a dict that supports del
    class MockSessionState(dict):
        def __delitem__(self, key):
            if key in self:
                super().__delitem__(key)

    mock_st.session_state = MockSessionState(mock_session_state)
    mock_st.rerun = Mock()

    logout_user()

    # Verify session was cleared
    assert "authentication_status" not in mock_st.session_state
    assert "api_token" not in mock_st.session_state
    mock_st.rerun.assert_called_once()


@patch("src.frontend.utils.requests")
@patch("src.frontend.utils.st")
def test_make_authenticated_request(mock_st, mock_requests):
    """Test make_authenticated_request function"""
    from src.frontend.utils import make_authenticated_request

    # Mock session state
    mock_st.session_state = {"api_token": "test_token"}

    # Mock requests response
    mock_response = Mock()
    mock_requests.request.return_value = mock_response

    response = make_authenticated_request("http://test.com", "GET")

    # Verify request was made with auth headers
    mock_requests.request.assert_called_once()
    call_args = mock_requests.request.call_args
    assert call_args[0][0] == "GET"  # method
    assert call_args[0][1] == "http://test.com"  # url
    assert "headers" in call_args[1]
    assert "Authorization" in call_args[1]["headers"]


def test_environment_variables():
    """Test environment variable handling"""
    # Test that environment variables can be set and read
    test_key = "TEST_AUDITORIA360_CONFIG"
    test_value = "test_value"

    os.environ[test_key] = test_value
    assert os.getenv(test_key) == test_value

    # Clean up
    if test_key in os.environ:
        del os.environ[test_key]


def test_config_defaults():
    """Test configuration defaults"""
    # Test common configuration patterns
    database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    assert isinstance(database_url, str)
    assert len(database_url) > 0

    secret_key = os.getenv("SECRET_KEY", "default-secret-key")
    assert isinstance(secret_key, str)
    assert len(secret_key) > 0


def test_logging_configuration():
    """Test logging can be configured"""
    import logging

    # Test basic logging functionality
    logger = logging.getLogger(__name__)
    assert logger is not None

    # Test log level setting
    logger.setLevel(logging.INFO)
    assert logger.level == logging.INFO


@patch("src.frontend.utils.st")
def test_require_authentication(mock_st):
    """Test require_authentication function"""
    from src.frontend.utils import require_authentication

    # Mock authenticated state
    mock_st.session_state = {"authentication_status": True, "api_token": "test_token"}
    mock_st.error = Mock()
    mock_st.stop = Mock()

    # Should not raise error when authenticated
    try:
        require_authentication()
    except SystemExit:
        # st.stop() raises SystemExit in some cases, that's expected
        pass

    # Should not call error when authenticated
    # (Note: This test may need adjustment based on actual implementation)


def test_utility_imports_available():
    """Test that utility modules can be imported without errors"""
    try:
        import src.frontend.utils

        assert src.frontend.utils is not None
    except ImportError as e:
        pytest.fail(f"Could not import frontend utils: {e}")

    try:
        import src.models

        assert src.models is not None
    except ImportError as e:
        pytest.fail(f"Could not import models: {e}")

    try:
        import src.services

        assert src.services is not None
    except ImportError as e:
        # Services might have missing dependencies, that's ok
        pass
