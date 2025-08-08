"""
Integration tests for health_check.py script
Tests the health checking functionality and its integration with the system
"""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add scripts path to system path
scripts_path = Path(__file__).parent.parent.parent / "scripts" / "python"
sys.path.insert(0, str(scripts_path))

try:
    from health_check import HealthChecker
    from health_check import main as health_main

    HEALTH_CHECK_AVAILABLE = True
except ImportError as e:
    HEALTH_CHECK_AVAILABLE = False
    pytest.skip(f"health_check module not available: {e}", allow_module_level=True)


class TestHealthCheckIntegration:
    """Integration tests for health check script"""

    @pytest.fixture
    def health_checker(self):
        """Create a HealthChecker instance for testing"""
        return HealthChecker()

    def test_health_checker_initialization(self, health_checker):
        """Test that HealthChecker initializes correctly"""
        assert hasattr(health_checker, "checks")
        assert hasattr(health_checker, "results")
        assert isinstance(health_checker.checks, list)
        assert isinstance(health_checker.results, list)

    @pytest.mark.asyncio
    async def test_database_health_check(self, health_checker):
        """Test database health check functionality"""
        result = await health_checker.check_database_health()
        assert isinstance(result, bool)
        # In the implementation, this always returns True (simulation)
        assert result is True

    @pytest.mark.asyncio
    async def test_storage_health_check(self, health_checker):
        """Test storage health check functionality"""
        result = await health_checker.check_storage_health()
        assert isinstance(result, bool)
        # In the implementation, this always returns True (simulation)
        assert result is True

    @pytest.mark.asyncio
    async def test_api_health_check_connection_error(self, health_checker):
        """Test API health check with connection error"""
        # Since we're testing locally without a running server, this should return False
        result = await health_checker.check_api_health()
        assert isinstance(result, bool)
        # Expected to fail since no server is running
        assert result is False

    @pytest.mark.asyncio
    async def test_run_all_checks(self, health_checker):
        """Test running all health checks and getting structured results"""
        results = await health_checker.run_all_checks()

        assert isinstance(results, list)
        assert len(results) == 3  # API, Database, Storage

        # Check that all required fields are present
        for result in results:
            assert "name" in result
            assert "status" in result
            assert "timestamp" in result
            assert result["name"] in ["API", "Database", "Storage"]
            assert result["status"] in ["healthy", "unhealthy", "error"]

    @pytest.mark.asyncio
    async def test_health_check_response_times(self, health_checker):
        """Test that health checks include response time measurements"""
        results = await health_checker.run_all_checks()

        for result in results:
            if result["status"] != "error":
                assert "response_time_ms" in result
                assert isinstance(result["response_time_ms"], (int, float))
                assert result["response_time_ms"] >= 0

    @pytest.mark.asyncio
    async def test_health_check_main_function(self):
        """Test the main function that outputs JSON results"""
        # Capture the output instead of printing
        with patch("builtins.print") as mock_print:
            await health_main()

            # Verify that print was called
            assert mock_print.called

            # Get the printed output and verify it's valid JSON
            printed_output = mock_print.call_args[0][0]
            parsed_output = json.loads(printed_output)

            # Verify JSON structure
            assert "timestamp" in parsed_output
            assert "overall_status" in parsed_output
            assert "checks" in parsed_output
            assert parsed_output["overall_status"] in ["healthy", "unhealthy"]
            assert isinstance(parsed_output["checks"], list)

    @pytest.mark.asyncio
    async def test_health_check_error_handling(self, health_checker):
        """Test error handling in health checks"""

        # Mock a check function to raise an exception
        async def failing_check():
            raise Exception("Test error")

        # Replace one of the check methods with the failing one
        original_method = health_checker.check_database_health
        health_checker.check_database_health = failing_check

        try:
            results = await health_checker.run_all_checks()

            # Find the database check result
            db_result = next(r for r in results if r["name"] == "Database")
            assert db_result["status"] == "error"
            assert "error" in db_result
            assert db_result["error"] == "Test error"
        finally:
            # Restore the original method
            health_checker.check_database_health = original_method

    def test_health_check_script_structure(self):
        """Test that the health check script has the expected structure"""
        assert hasattr(HealthChecker, "__init__")
        assert hasattr(HealthChecker, "check_api_health")
        assert hasattr(HealthChecker, "check_database_health")
        assert hasattr(HealthChecker, "check_storage_health")
        assert hasattr(HealthChecker, "run_all_checks")

    @pytest.mark.asyncio
    async def test_health_check_concurrent_execution(self, health_checker):
        """Test that health checks can run concurrently"""
        import time

        start_time = time.time()

        # Run checks multiple times concurrently
        tasks = [health_checker.run_all_checks() for _ in range(3)]
        results = await asyncio.gather(*tasks)

        end_time = time.time()

        # Verify all results are valid
        assert len(results) == 3
        for result_set in results:
            assert len(result_set) == 3

        # Concurrent execution should be faster than sequential
        # (This is a rough check, might need adjustment based on timing)
        assert end_time - start_time < 2.0  # Should complete well under 2 seconds

    def test_health_check_integration_with_system(self):
        """Test that health check integrates properly with the system"""
        # Verify the script can be imported and used
        assert HEALTH_CHECK_AVAILABLE

        # Verify the main function exists for CLI usage
        assert callable(health_main)

        # Verify required modules are available
        import aiohttp

        assert aiohttp.__version__  # Ensure aiohttp is available


if __name__ == "__main__":
    pytest.main([__file__])
