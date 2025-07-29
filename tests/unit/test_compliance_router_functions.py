"""
Focused unit tests for Audit/Compliance Router functions
Day 3: Expanding compliance router tests to increase coverage from 40% to >80%
"""

import os
import sys
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Import the actual functions from the router
from src.api.routers.audit import (
    create_compliance_rule,
    execute_audit,
    list_audit_executions,
    list_audit_findings,
    list_compliance_reports,
)


class TestAuditRouterFunctions:
    """Test suite for individual audit router functions"""

    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return MagicMock()

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

    # Test execute_audit function
    @pytest.mark.asyncio
    async def test_execute_audit_admin_success(self, mock_admin_user, mock_db):
        """Test execute_audit with admin user - should succeed"""
        result = await execute_audit(current_user=mock_admin_user, db=mock_db)

        assert "message" in result
        assert "Audit execution endpoint" in result["message"]

    @pytest.mark.asyncio
    async def test_execute_audit_contador_success(self, mock_contador_user, mock_db):
        """Test execute_audit with contador user - should succeed"""
        result = await execute_audit(current_user=mock_contador_user, db=mock_db)

        assert "message" in result
        assert "Audit execution endpoint" in result["message"]

    @pytest.mark.asyncio
    async def test_execute_audit_regular_user_forbidden(
        self, mock_regular_user, mock_db
    ):
        """Test execute_audit with regular user - should raise 403"""
        with pytest.raises(HTTPException) as exc_info:
            await execute_audit(current_user=mock_regular_user, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert exc_info.value.detail == "Not enough permissions"

    @pytest.mark.asyncio
    async def test_execute_audit_unauthorized_role(self, mock_db):
        """Test execute_audit with unauthorized role"""
        unauthorized_user = MagicMock()
        unauthorized_user.role = "guest"

        with pytest.raises(HTTPException) as exc_info:
            await execute_audit(current_user=unauthorized_user, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_execute_audit_none_role(self, mock_db):
        """Test execute_audit with None role"""
        user_none_role = MagicMock()
        user_none_role.role = None

        with pytest.raises(HTTPException) as exc_info:
            await execute_audit(current_user=user_none_role, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    # Test list_audit_executions function
    @pytest.mark.asyncio
    async def test_list_audit_executions_success(self, mock_admin_user, mock_db):
        """Test list_audit_executions - should succeed"""
        result = await list_audit_executions(
            skip=0, limit=100, current_user=mock_admin_user, db=mock_db
        )

        assert "message" in result
        assert "Audit executions list endpoint" in result["message"]

    @pytest.mark.asyncio
    async def test_list_audit_executions_with_custom_pagination(
        self, mock_admin_user, mock_db
    ):
        """Test list_audit_executions with custom pagination"""
        result = await list_audit_executions(
            skip=10, limit=50, current_user=mock_admin_user, db=mock_db
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_audit_executions_regular_user(self, mock_regular_user, mock_db):
        """Test list_audit_executions with regular user - should work"""
        result = await list_audit_executions(
            skip=0, limit=100, current_user=mock_regular_user, db=mock_db
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_audit_executions_zero_limit(self, mock_admin_user, mock_db):
        """Test list_audit_executions with zero limit"""
        result = await list_audit_executions(
            skip=0, limit=0, current_user=mock_admin_user, db=mock_db
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_audit_executions_large_numbers(self, mock_admin_user, mock_db):
        """Test list_audit_executions with large pagination numbers"""
        result = await list_audit_executions(
            skip=1000, limit=10000, current_user=mock_admin_user, db=mock_db
        )

        assert "message" in result

    # Test list_audit_findings function
    @pytest.mark.asyncio
    async def test_list_audit_findings_success(self, mock_admin_user, mock_db):
        """Test list_audit_findings - should succeed"""
        result = await list_audit_findings(
            skip=0,
            limit=100,
            severity=None,
            resolved=None,
            current_user=mock_admin_user,
            db=mock_db,
        )

        assert "message" in result
        assert "Audit findings list endpoint" in result["message"]

    @pytest.mark.asyncio
    async def test_list_audit_findings_with_severity_filter(
        self, mock_admin_user, mock_db
    ):
        """Test list_audit_findings with severity filter"""
        result = await list_audit_findings(
            skip=0,
            limit=100,
            severity="high",
            resolved=None,
            current_user=mock_admin_user,
            db=mock_db,
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_audit_findings_with_resolved_filter(
        self, mock_admin_user, mock_db
    ):
        """Test list_audit_findings with resolved filter"""
        result = await list_audit_findings(
            skip=0,
            limit=100,
            severity=None,
            resolved=True,
            current_user=mock_admin_user,
            db=mock_db,
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_audit_findings_with_both_filters(
        self, mock_admin_user, mock_db
    ):
        """Test list_audit_findings with both filters"""
        result = await list_audit_findings(
            skip=5,
            limit=25,
            severity="critical",
            resolved=False,
            current_user=mock_admin_user,
            db=mock_db,
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_audit_findings_contador_user(self, mock_contador_user, mock_db):
        """Test list_audit_findings with contador user"""
        result = await list_audit_findings(
            skip=0,
            limit=100,
            severity=None,
            resolved=None,
            current_user=mock_contador_user,
            db=mock_db,
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_audit_findings_regular_user(self, mock_regular_user, mock_db):
        """Test list_audit_findings with regular user"""
        result = await list_audit_findings(
            skip=0,
            limit=100,
            severity=None,
            resolved=None,
            current_user=mock_regular_user,
            db=mock_db,
        )

        assert "message" in result

    # Test create_compliance_rule function
    @pytest.mark.asyncio
    async def test_create_compliance_rule_admin_success(self, mock_admin_user, mock_db):
        """Test create_compliance_rule with admin user - should succeed"""
        result = await create_compliance_rule(current_user=mock_admin_user, db=mock_db)

        assert "message" in result
        assert "Compliance rule creation endpoint" in result["message"]

    @pytest.mark.asyncio
    async def test_create_compliance_rule_contador_forbidden(
        self, mock_contador_user, mock_db
    ):
        """Test create_compliance_rule with contador user - should raise 403"""
        with pytest.raises(HTTPException) as exc_info:
            await create_compliance_rule(current_user=mock_contador_user, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert exc_info.value.detail == "Not enough permissions"

    @pytest.mark.asyncio
    async def test_create_compliance_rule_regular_user_forbidden(
        self, mock_regular_user, mock_db
    ):
        """Test create_compliance_rule with regular user - should raise 403"""
        with pytest.raises(HTTPException) as exc_info:
            await create_compliance_rule(current_user=mock_regular_user, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_compliance_rule_guest_forbidden(self, mock_db):
        """Test create_compliance_rule with guest user - should raise 403"""
        guest_user = MagicMock()
        guest_user.role = "guest"

        with pytest.raises(HTTPException) as exc_info:
            await create_compliance_rule(current_user=guest_user, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_compliance_rule_manager_forbidden(self, mock_db):
        """Test create_compliance_rule with manager user - should raise 403"""
        manager_user = MagicMock()
        manager_user.role = "manager"

        with pytest.raises(HTTPException) as exc_info:
            await create_compliance_rule(current_user=manager_user, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    # Test list_compliance_reports function
    @pytest.mark.asyncio
    async def test_list_compliance_reports_success(self, mock_admin_user, mock_db):
        """Test list_compliance_reports - should succeed"""
        result = await list_compliance_reports(current_user=mock_admin_user, db=mock_db)

        assert "message" in result
        assert "Compliance reports list endpoint" in result["message"]

    @pytest.mark.asyncio
    async def test_list_compliance_reports_contador(self, mock_contador_user, mock_db):
        """Test list_compliance_reports with contador user"""
        result = await list_compliance_reports(
            current_user=mock_contador_user, db=mock_db
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_compliance_reports_regular_user(
        self, mock_regular_user, mock_db
    ):
        """Test list_compliance_reports with regular user"""
        result = await list_compliance_reports(
            current_user=mock_regular_user, db=mock_db
        )

        assert "message" in result

    @pytest.mark.asyncio
    async def test_list_compliance_reports_guest_user(self, mock_db):
        """Test list_compliance_reports with guest user"""
        guest_user = MagicMock()
        guest_user.role = "guest"

        result = await list_compliance_reports(current_user=guest_user, db=mock_db)

        assert "message" in result

    # Test edge cases and error conditions
    @pytest.mark.asyncio
    async def test_execute_audit_no_role_attribute(self, mock_db):
        """Test execute_audit with user that has no role attribute"""
        user_no_role = MagicMock()
        del user_no_role.role

        with pytest.raises(AttributeError):
            await execute_audit(current_user=user_no_role, db=mock_db)

    @pytest.mark.asyncio
    async def test_create_compliance_rule_no_role_attribute(self, mock_db):
        """Test create_compliance_rule with user that has no role attribute"""
        user_no_role = MagicMock()
        del user_no_role.role

        with pytest.raises(AttributeError):
            await create_compliance_rule(current_user=user_no_role, db=mock_db)

    @pytest.mark.asyncio
    async def test_execute_audit_empty_role(self, mock_db):
        """Test execute_audit with empty role"""
        user_empty_role = MagicMock()
        user_empty_role.role = ""

        with pytest.raises(HTTPException) as exc_info:
            await execute_audit(current_user=user_empty_role, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_compliance_rule_empty_role(self, mock_db):
        """Test create_compliance_rule with empty role"""
        user_empty_role = MagicMock()
        user_empty_role.role = ""

        with pytest.raises(HTTPException) as exc_info:
            await create_compliance_rule(current_user=user_empty_role, db=mock_db)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    # Test parameter combinations
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "skip,limit",
        [
            (0, 1),
            (0, 50),
            (0, 100),
            (10, 20),
            (100, 500),
            (0, 999999),  # Large limit
            (999999, 1),  # Large skip
        ],
    )
    async def test_list_audit_executions_parameter_combinations(
        self, mock_admin_user, mock_db, skip, limit
    ):
        """Test list_audit_executions with various parameter combinations"""
        result = await list_audit_executions(
            skip=skip, limit=limit, current_user=mock_admin_user, db=mock_db
        )

        assert "message" in result

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "severity,resolved",
        [
            ("low", True),
            ("medium", False),
            ("high", None),
            ("critical", True),
            (None, False),
            (None, True),
            (None, None),
        ],
    )
    async def test_list_audit_findings_filter_combinations(
        self, mock_admin_user, mock_db, severity, resolved
    ):
        """Test list_audit_findings with various filter combinations"""
        result = await list_audit_findings(
            skip=0,
            limit=100,
            severity=severity,
            resolved=resolved,
            current_user=mock_admin_user,
            db=mock_db,
        )

        assert "message" in result

    # Test role-based access patterns
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "role,should_succeed",
        [
            ("administrador", True),
            ("contador", True),
            ("usuario", False),
            ("guest", False),
            ("manager", False),
            ("supervisor", False),
            ("auditor", False),
        ],
    )
    async def test_execute_audit_role_access_matrix(
        self, mock_db, role, should_succeed
    ):
        """Test execute_audit access control with various roles"""
        user = MagicMock()
        user.role = role

        if should_succeed:
            result = await execute_audit(current_user=user, db=mock_db)
            assert "message" in result
        else:
            with pytest.raises(HTTPException) as exc_info:
                await execute_audit(current_user=user, db=mock_db)
            assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "role",
        ["administrador", "contador", "usuario", "guest", "manager", "supervisor"],
    )
    async def test_list_functions_all_roles_allowed(self, mock_db, role):
        """Test that list functions allow all roles"""
        user = MagicMock()
        user.role = role

        # All these should succeed regardless of role
        result1 = await list_audit_executions(
            skip=0, limit=100, current_user=user, db=mock_db
        )
        result2 = await list_audit_findings(
            skip=0,
            limit=100,
            severity=None,
            resolved=None,
            current_user=user,
            db=mock_db,
        )
        result3 = await list_compliance_reports(current_user=user, db=mock_db)

        assert "message" in result1
        assert "message" in result2
        assert "message" in result3

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "role,should_succeed",
        [
            ("administrador", True),
            ("contador", False),
            ("usuario", False),
            ("guest", False),
            ("manager", False),
            ("supervisor", False),
            ("auditor", False),
        ],
    )
    async def test_create_compliance_rule_role_access_matrix(
        self, mock_db, role, should_succeed
    ):
        """Test create_compliance_rule access control with various roles"""
        user = MagicMock()
        user.role = role

        if should_succeed:
            result = await create_compliance_rule(current_user=user, db=mock_db)
            assert "message" in result
        else:
            with pytest.raises(HTTPException) as exc_info:
                await create_compliance_rule(current_user=user, db=mock_db)
            assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


if __name__ == "__main__":
    pytest.main([__file__])
