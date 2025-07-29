"""
Tests for serverless automation modules
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add automation modules to path
automation_path = Path(__file__).parent.parent / "automation"
sys.path.insert(0, str(automation_path))


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(
        os.environ,
        {
            "API_BASE_URL": "https://test-api.example.com",
            "API_AUTH_TOKEN": "test-token-123",
            "BACKUP_STORAGE_URL": "https://test-storage.example.com",
            "STORAGE_TOKEN": "storage-token-123",
            "ENVIRONMENT": "test",
        },
    ):
        yield


@pytest.fixture
def mock_httpx_client():
    """Mock httpx AsyncClient"""
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()

        # Configure the context manager properly
        async def mock_aenter():
            return mock_instance

        async def mock_aexit(*args):
            pass

        mock_client.return_value.__aenter__ = mock_aenter
        mock_client.return_value.__aexit__ = mock_aexit

        yield mock_instance


class TestPayrollRPAServerless:
    """Test payroll RPA automation"""

    @pytest.mark.asyncio
    async def test_authentication_with_token(self, mock_env_vars):
        """Test authentication when token is provided"""
        from rpa_folha import PayrollRPAServerless

        rpa = PayrollRPAServerless()
        token = await rpa.authenticate()
        assert token == "test-token-123"

    @pytest.mark.asyncio
    async def test_authentication_with_credentials(
        self, mock_env_vars, mock_httpx_client
    ):
        """Test authentication with username/password"""
        # Remove token to force credential auth
        with patch.dict(os.environ, {"API_AUTH_TOKEN": ""}, clear=False):
            from rpa_folha import PayrollRPAServerless

            # Mock successful auth response
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(
                return_value={"access_token": "new-token-456"}
            )
            mock_httpx_client.post = AsyncMock(return_value=mock_response)

            rpa = PayrollRPAServerless()
            token = await rpa.authenticate()
            assert token == "new-token-456"

    @pytest.mark.asyncio
    async def test_process_pending_payrolls(self, mock_env_vars, mock_httpx_client):
        """Test processing pending payroll items"""
        from rpa_folha import PayrollRPAServerless

        # Mock API responses
        pending_response = MagicMock()
        pending_response.raise_for_status = MagicMock()
        pending_response.json = MagicMock(
            return_value=[
                {"id": 1, "base_salary": 5000, "overtime_hours": 10, "deductions": 500},
                {"id": 2, "base_salary": 6000, "overtime_hours": 5, "deductions": 600},
            ]
        )

        update_response = MagicMock()
        update_response.raise_for_status = MagicMock()

        mock_httpx_client.get = AsyncMock(return_value=pending_response)
        mock_httpx_client.patch = AsyncMock(return_value=update_response)

        rpa = PayrollRPAServerless()
        results = await rpa.process_pending_payrolls()

        assert results["processed"] == 2
        assert results["failed"] == 0
        assert len(results["errors"]) == 0

    @pytest.mark.asyncio
    async def test_payroll_calculations(self, mock_env_vars):
        """Test payroll calculation logic"""
        from rpa_folha import PayrollRPAServerless

        rpa = PayrollRPAServerless()
        item = {"base_salary": 5000, "overtime_hours": 10, "deductions": 500}

        calculations = await rpa._calculate_payroll(item)

        # Expected: overtime_pay = 10 * (5000/220 * 1.5) = 340.91
        # gross_pay = 5000 + 340.91 = 5340.91
        # net_pay = 5340.91 - 500 = 4840.91

        assert calculations["base_salary"] == 5000
        assert calculations["overtime_pay"] == pytest.approx(340.91, rel=1e-2)
        assert calculations["gross_pay"] == pytest.approx(5340.91, rel=1e-2)
        assert calculations["net_pay"] == pytest.approx(4840.91, rel=1e-2)


class TestScheduledReportsServerless:
    """Test scheduled reports automation"""

    @pytest.mark.asyncio
    async def test_generate_daily_report(self, mock_env_vars, mock_httpx_client):
        """Test daily report generation"""
        from schedule_reports import ScheduledReportsServerless

        # Mock API responses
        audit_response = AsyncMock()
        audit_response.raise_for_status.return_value = None
        audit_response.json.return_value = {
            "total_audits": 50,
            "completed_audits": 45,
            "pending_audits": 5,
            "details": [],
        }

        compliance_response = AsyncMock()
        compliance_response.raise_for_status.return_value = None
        compliance_response.json.return_value = {
            "compliance_score": 0.92,
            "critical_issues": 2,
            "resolved_issues": 8,
            "details": [],
        }

        save_response = AsyncMock()
        save_response.raise_for_status.return_value = None

        mock_httpx_client.get.side_effect = [audit_response, compliance_response]
        mock_httpx_client.post.return_value = save_response

        scheduler = ScheduledReportsServerless()

        # Mock file writing
        with patch("builtins.open", MagicMock()):
            with patch("json.dump"):
                report = await scheduler.generate_daily_report()

        assert report["type"] == "daily_report"
        assert report["summary"]["total_audits"] == 50
        assert report["summary"]["compliance_score"] == 0.92

    @pytest.mark.asyncio
    async def test_generate_weekly_report(self, mock_env_vars, mock_httpx_client):
        """Test weekly report generation"""
        from schedule_reports import ScheduledReportsServerless

        # Mock responses
        mock_responses = [
            {"total_audits": 300, "completion_rate": 0.85},
            {"average_score": 0.88, "improvement": 0.03},
            {"high_risk_count": 12, "overall_score": 0.75},
        ]

        for i, response_data in enumerate(mock_responses):
            response = AsyncMock()
            response.raise_for_status.return_value = None
            response.json.return_value = response_data

            if i == 0:
                mock_httpx_client.get.return_value = response
            else:
                mock_httpx_client.get.side_effect = [
                    mock_httpx_client.get.return_value,
                    response,
                ]

        save_response = AsyncMock()
        save_response.raise_for_status.return_value = None
        mock_httpx_client.post.return_value = save_response

        scheduler = ScheduledReportsServerless()

        with patch("builtins.open", MagicMock()):
            with patch("json.dump"):
                report = await scheduler.generate_weekly_report()

        assert report["type"] == "weekly_report"
        assert "recommendations" in report


class TestBackupRoutineServerless:
    """Test backup routine automation"""

    @pytest.mark.asyncio
    async def test_backup_database(self, mock_env_vars, mock_httpx_client):
        """Test database backup functionality"""
        from backup_routine import BackupRoutineServerless

        # Mock export response
        export_response = AsyncMock()
        export_response.raise_for_status.return_value = None
        export_response.json.return_value = {
            "data": {"table1": [{"id": 1, "name": "test"}]},
            "metadata": {"tables": ["table1"], "total_records": 1},
        }

        mock_httpx_client.post.return_value = export_response

        backup_service = BackupRoutineServerless()

        # Mock storage upload
        with patch.object(backup_service, "_upload_to_storage") as mock_upload:
            mock_upload.return_value = {
                "method": "local",
                "path": "/tmp/test",
                "size": 100,
            }

            result = await backup_service.backup_database()

        assert result["status"] == "success"
        assert "filename" in result
        assert result["metadata"]["record_count"] == 1

    @pytest.mark.asyncio
    async def test_should_backup_file(self, mock_env_vars):
        """Test file backup filtering logic"""
        from backup_routine import BackupRoutineServerless

        backup_service = BackupRoutineServerless()

        # Should backup critical files under size limit
        assert (
            backup_service._should_backup_file({"name": "important.json", "size": 1024})
            == True
        )

        assert (
            backup_service._should_backup_file(
                {"name": "report.pdf", "size": 50 * 1024}
            )
            == True
        )

        # Should not backup non-critical files
        assert (
            backup_service._should_backup_file({"name": "image.jpg", "size": 1024})
            == False
        )

        # Should not backup large files
        assert (
            backup_service._should_backup_file(
                {"name": "large.json", "size": 200 * 1024 * 1024}  # 200MB
            )
            == False
        )


class TestAutomationIntegration:
    """Test automation module integration"""

    @pytest.mark.asyncio
    async def test_run_payroll_automation_github_actions(self, mock_env_vars):
        """Test payroll automation with GitHub Actions environment"""
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}):
            with patch("rpa_folha.PayrollRPAServerless") as mock_class:
                mock_instance = AsyncMock()
                mock_instance.process_pending_payrolls.return_value = {
                    "processed": 5,
                    "failed": 0,
                }
                mock_instance.generate_payroll_reports.return_value = {"reports": 3}
                mock_class.return_value = mock_instance

                from rpa_folha import run_payroll_automation

                # Capture printed output
                with patch("builtins.print") as mock_print:
                    result = await run_payroll_automation()

                assert result["status"] == "success"
                # Verify GitHub Actions output was printed
                mock_print.assert_called()

    @pytest.mark.asyncio
    async def test_run_scheduled_reports_vercel(self, mock_env_vars):
        """Test scheduled reports with Vercel environment"""
        with patch.dict(os.environ, {"VERCEL": "true"}):
            with patch("schedule_reports.ScheduledReportsServerless") as mock_class:
                mock_instance = AsyncMock()
                mock_instance.generate_daily_report.return_value = {
                    "type": "daily_report"
                }
                mock_class.return_value = mock_instance

                from schedule_reports import run_scheduled_reports

                with patch("builtins.print") as mock_print:
                    result = await run_scheduled_reports("daily")

                assert result["type"] == "daily_report"
                mock_print.assert_called()

    def test_github_actions_workflow_compatibility(self):
        """Test that automation modules are compatible with GitHub Actions"""
        # Test that modules can be imported without side effects
        try:
            import backup_routine
            import rpa_folha
            import schedule_reports

            # Test that main functions exist
            assert hasattr(rpa_folha, "run_payroll_automation")
            assert hasattr(schedule_reports, "run_scheduled_reports")
            assert hasattr(backup_routine, "run_backup_routine")

            # Test that functions are async
            assert asyncio.iscoroutinefunction(rpa_folha.run_payroll_automation)
            assert asyncio.iscoroutinefunction(schedule_reports.run_scheduled_reports)
            assert asyncio.iscoroutinefunction(backup_routine.run_backup_routine)

        except ImportError as e:
            pytest.fail(f"Automation modules not properly importable: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
