"""
Comprehensive unit tests for Audit/Compliance Router
Day 3: Expanding compliance router tests to increase coverage from 40% to >80%
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI

# Import the router directly for testing
from src.api.routers.audit import router

# Create a test app with just the audit router
test_app = FastAPI()
test_app.include_router(router, prefix="/audit")


class TestAuditRouter:
    """Comprehensive test suite for audit/compliance router"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(test_app)

    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        db = MagicMock()
        return db

    @pytest.fixture
    def mock_admin_user(self):
        """Mock admin user"""
        user = MagicMock()
        user.id = 1
        user.role = "administrador"
        user.username = "admin_user"
        return user

    @pytest.fixture
    def mock_contador_user(self):
        """Mock contador user"""
        user = MagicMock()
        user.id = 2
        user.role = "contador"
        user.username = "contador_user"
        return user

    @pytest.fixture
    def mock_regular_user(self):
        """Mock regular user"""
        user = MagicMock()
        user.id = 3
        user.role = "usuario"
        user.username = "regular_user"
        return user

    # Test execute_audit endpoint
    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_execute_audit_success_admin(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test execute_audit with admin user - should succeed"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.post("/audit/execute")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "Audit execution endpoint" in response.json()["message"]

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_execute_audit_success_contador(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_contador_user
    ):
        """Test execute_audit with contador user - should succeed"""
        mock_get_current_user.return_value = mock_contador_user
        mock_get_db.return_value = mock_db

        response = client.post("/audit/execute")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "Audit execution endpoint" in response.json()["message"]

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_execute_audit_forbidden_regular_user(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_regular_user
    ):
        """Test execute_audit with regular user - should be forbidden"""
        mock_get_current_user.return_value = mock_regular_user
        mock_get_db.return_value = mock_db

        response = client.post("/audit/execute")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Not enough permissions"

    @patch("src.api.routers.audit.get_current_user")
    def test_execute_audit_authentication_required(self, mock_get_current_user, client):
        """Test execute_audit without authentication - should fail"""
        mock_get_current_user.side_effect = Exception("Authentication required")

        with pytest.raises(Exception):
            client.post("/audit/execute")

    # Test list_audit_executions endpoint
    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_executions_success(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test list_audit_executions - should succeed"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/executions")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "Audit executions list endpoint" in response.json()["message"]

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_executions_with_pagination(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test list_audit_executions with pagination parameters"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/executions?skip=10&limit=50")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_executions_contador_access(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_contador_user
    ):
        """Test list_audit_executions with contador user"""
        mock_get_current_user.return_value = mock_contador_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/executions")

        assert response.status_code == status.HTTP_200_OK

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_executions_regular_user_access(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_regular_user
    ):
        """Test list_audit_executions with regular user - should still work"""
        mock_get_current_user.return_value = mock_regular_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/executions")

        assert response.status_code == status.HTTP_200_OK

    # Test list_audit_findings endpoint
    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_findings_success(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test list_audit_findings - should succeed"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/findings")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "Audit findings list endpoint" in response.json()["message"]

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_findings_with_filters(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test list_audit_findings with severity and resolved filters"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.get(
            "/audit/findings?severity=high&resolved=false&skip=5&limit=25"
        )

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_findings_severity_filter_only(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_contador_user
    ):
        """Test list_audit_findings with only severity filter"""
        mock_get_current_user.return_value = mock_contador_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/findings?severity=critical")

        assert response.status_code == status.HTTP_200_OK

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_findings_resolved_filter_only(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test list_audit_findings with only resolved filter"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/findings?resolved=true")

        assert response.status_code == status.HTTP_200_OK

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_audit_findings_invalid_bool_parameter(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test list_audit_findings with invalid boolean parameter"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        # This should still work as FastAPI will handle the validation
        response = client.get("/audit/findings?resolved=maybe")

        # FastAPI validation error for invalid boolean
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test create_compliance_rule endpoint
    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_create_compliance_rule_success_admin(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test create_compliance_rule with admin user - should succeed"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.post("/audit/rules")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "Compliance rule creation endpoint" in response.json()["message"]

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_create_compliance_rule_forbidden_contador(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_contador_user
    ):
        """Test create_compliance_rule with contador user - should be forbidden"""
        mock_get_current_user.return_value = mock_contador_user
        mock_get_db.return_value = mock_db

        response = client.post("/audit/rules")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Not enough permissions"

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_create_compliance_rule_forbidden_regular_user(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_regular_user
    ):
        """Test create_compliance_rule with regular user - should be forbidden"""
        mock_get_current_user.return_value = mock_regular_user
        mock_get_db.return_value = mock_db

        response = client.post("/audit/rules")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Not enough permissions"

    @patch("src.api.routers.audit.get_current_user")
    def test_create_compliance_rule_authentication_required(
        self, mock_get_current_user, client
    ):
        """Test create_compliance_rule without authentication - should fail"""
        mock_get_current_user.side_effect = Exception("Authentication required")

        with pytest.raises(Exception):
            client.post("/audit/rules")

    # Test list_compliance_reports endpoint
    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_compliance_reports_success(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test list_compliance_reports - should succeed"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/reports")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "Compliance reports list endpoint" in response.json()["message"]

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_compliance_reports_contador_access(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_contador_user
    ):
        """Test list_compliance_reports with contador user"""
        mock_get_current_user.return_value = mock_contador_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/reports")

        assert response.status_code == status.HTTP_200_OK

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_list_compliance_reports_regular_user_access(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_regular_user
    ):
        """Test list_compliance_reports with regular user"""
        mock_get_current_user.return_value = mock_regular_user
        mock_get_db.return_value = mock_db

        response = client.get("/audit/reports")

        assert response.status_code == status.HTTP_200_OK

    # Test edge cases and error handling
    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_endpoints_with_database_error(
        self, mock_get_db, mock_get_current_user, client, mock_admin_user
    ):
        """Test endpoints when database connection fails"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.side_effect = Exception("Database connection failed")

        # Test all endpoints with database error
        endpoints = [
            ("POST", "/audit/execute"),
            ("GET", "/audit/executions"),
            ("GET", "/audit/findings"),
            ("POST", "/audit/rules"),
            ("GET", "/audit/reports"),
        ]

        for method, endpoint in endpoints:
            with pytest.raises(Exception):
                if method == "POST":
                    client.post(endpoint)
                else:
                    client.get(endpoint)

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_execute_audit_with_malformed_user(
        self, mock_get_db, mock_get_current_user, client, mock_db
    ):
        """Test execute_audit with user that has no role attribute"""
        malformed_user = MagicMock()
        del malformed_user.role  # Remove role attribute
        mock_get_current_user.return_value = malformed_user
        mock_get_db.return_value = mock_db

        with pytest.raises(AttributeError):
            client.post("/audit/execute")

    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_create_compliance_rule_with_malformed_user(
        self, mock_get_db, mock_get_current_user, client, mock_db
    ):
        """Test create_compliance_rule with user that has no role attribute"""
        malformed_user = MagicMock()
        del malformed_user.role  # Remove role attribute
        mock_get_current_user.return_value = malformed_user
        mock_get_db.return_value = mock_db

        with pytest.raises(AttributeError):
            client.post("/audit/rules")

    # Test parameter validation
    def test_list_audit_executions_negative_skip(self, client):
        """Test list_audit_executions with negative skip parameter"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role="administrador")
            mock_db.return_value = MagicMock()

            response = client.get("/audit/executions?skip=-1")

            # FastAPI should handle parameter validation
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_audit_executions_negative_limit(self, client):
        """Test list_audit_executions with negative limit parameter"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role="administrador")
            mock_db.return_value = MagicMock()

            response = client.get("/audit/executions?limit=-1")

            # FastAPI should handle parameter validation
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_audit_findings_negative_skip(self, client):
        """Test list_audit_findings with negative skip parameter"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role="administrador")
            mock_db.return_value = MagicMock()

            response = client.get("/audit/findings?skip=-5")

            # FastAPI should handle parameter validation
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_list_audit_findings_negative_limit(self, client):
        """Test list_audit_findings with negative limit parameter"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role="administrador")
            mock_db.return_value = MagicMock()

            response = client.get("/audit/findings?limit=-10")

            # FastAPI should handle parameter validation
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test all role combinations for each endpoint
    @pytest.mark.parametrize(
        "user_role,expected_status",
        [
            ("administrador", status.HTTP_200_OK),
            ("contador", status.HTTP_200_OK),
            ("usuario", status.HTTP_403_FORBIDDEN),
            ("guest", status.HTTP_403_FORBIDDEN),
            ("manager", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_execute_audit_role_matrix(self, client, user_role, expected_status):
        """Test execute_audit with different user roles"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role=user_role)
            mock_db.return_value = MagicMock()

            response = client.post("/audit/execute")

            assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_role", ["administrador", "contador", "usuario", "guest", "manager"]
    )
    def test_list_audit_executions_role_matrix(self, client, user_role):
        """Test list_audit_executions with different user roles - all should succeed"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role=user_role)
            mock_db.return_value = MagicMock()

            response = client.get("/audit/executions")

            assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "user_role", ["administrador", "contador", "usuario", "guest", "manager"]
    )
    def test_list_audit_findings_role_matrix(self, client, user_role):
        """Test list_audit_findings with different user roles - all should succeed"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role=user_role)
            mock_db.return_value = MagicMock()

            response = client.get("/audit/findings")

            assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "user_role,expected_status",
        [
            ("administrador", status.HTTP_200_OK),
            ("contador", status.HTTP_403_FORBIDDEN),
            ("usuario", status.HTTP_403_FORBIDDEN),
            ("guest", status.HTTP_403_FORBIDDEN),
            ("manager", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_compliance_rule_role_matrix(
        self, client, user_role, expected_status
    ):
        """Test create_compliance_rule with different user roles"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role=user_role)
            mock_db.return_value = MagicMock()

            response = client.post("/audit/rules")

            assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_role", ["administrador", "contador", "usuario", "guest", "manager"]
    )
    def test_list_compliance_reports_role_matrix(self, client, user_role):
        """Test list_compliance_reports with different user roles - all should succeed"""
        with patch("src.api.routers.audit.get_current_user") as mock_user, patch(
            "src.api.routers.audit.get_db"
        ) as mock_db:

            mock_user.return_value = MagicMock(role=user_role)
            mock_db.return_value = MagicMock()

            response = client.get("/audit/reports")

            assert response.status_code == status.HTTP_200_OK

    # Test concurrent access scenarios
    @patch("src.api.routers.audit.get_current_user")
    @patch("src.api.routers.audit.get_db")
    def test_concurrent_audit_execution_requests(
        self, mock_get_db, mock_get_current_user, client, mock_db, mock_admin_user
    ):
        """Test multiple concurrent audit execution requests"""
        mock_get_current_user.return_value = mock_admin_user
        mock_get_db.return_value = mock_db

        # Simulate concurrent requests
        responses = []
        for _ in range(3):
            response = client.post("/audit/execute")
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK


if __name__ == "__main__":
    pytest.main([__file__])
