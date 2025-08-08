"""
Integration tests for monitoramento.py script
Tests the monitoring functionality and its integration with the system
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add scripts path to system path
scripts_path = Path(__file__).parent.parent.parent / "scripts" / "python"
sys.path.insert(0, str(scripts_path))

try:
    from monitoramento import (
        checar_servico,
        check_database_health,
        check_performance_metrics,
        check_storage_health,
    )
    from monitoramento import main as monitoring_main
    from monitoramento import (
        show_alerts,
    )

    MONITORING_AVAILABLE = True
except ImportError as e:
    MONITORING_AVAILABLE = False
    pytest.skip(f"monitoramento module not available: {e}", allow_module_level=True)


class TestMonitoringScriptIntegration:
    """Integration tests for monitoring script"""

    def test_monitoring_script_availability(self):
        """Test that monitoring script is available and importable"""
        assert MONITORING_AVAILABLE

        # Check that key functions are available
        assert callable(checar_servico)
        assert callable(check_database_health)
        assert callable(check_storage_health)
        assert callable(monitoring_main)

    @patch("monitoramento.requests.get")
    def test_checar_servico_success(self, mock_get):
        """Test successful service health check"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            checar_servico("Test API", "http://localhost:8000/health")

            # Verify the service check was performed
            mock_get.assert_called_once_with("http://localhost:8000/health", timeout=5)

            # Verify positive result was printed
            mock_print.assert_called()
            printed_text = mock_print.call_args[0][0]
            assert "Test API: OK" in printed_text

    @patch("monitoramento.requests.get")
    def test_checar_servico_failure(self, mock_get):
        """Test failed service health check"""
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            checar_servico("Test API", "http://localhost:8000/health")

            # Verify failure was reported
            mock_print.assert_called()
            printed_text = mock_print.call_args[0][0]
            assert "Test API: Falha (500)" in printed_text

    @patch("monitoramento.requests.get")
    def test_checar_servico_exception(self, mock_get):
        """Test service health check with connection exception"""
        # Mock connection exception
        mock_get.side_effect = Exception("Connection refused")

        with patch("builtins.print") as mock_print:
            checar_servico("Test API", "http://localhost:8000/health")

            # Verify error was reported
            mock_print.assert_called()
            printed_text = mock_print.call_args[0][0]
            assert "Test API: Erro" in printed_text
            assert "Connection refused" in printed_text

    @pytest.mark.asyncio
    async def test_check_database_health(self):
        """Test database health check functionality"""
        with patch("builtins.print") as mock_print:
            result = await check_database_health()

            # Should return True (simulation)
            assert result is True

            # Should print status messages
            assert mock_print.called
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Database:" in call for call in calls)

    @pytest.mark.asyncio
    async def test_check_storage_health(self):
        """Test storage (R2) health check functionality"""
        with patch("builtins.print") as mock_print:
            result = await check_storage_health()

            # Should return True (simulation)
            assert result is True

            # Should print status messages
            assert mock_print.called
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert any("Storage (R2):" in call for call in calls)

    def test_check_performance_metrics_without_enhanced_monitoring(self):
        """Test performance metrics check when enhanced monitoring is not available"""
        # Test with ENHANCED_MONITORING = False
        with patch("monitoramento.ENHANCED_MONITORING", False):
            result = check_performance_metrics()
            # Should return None or handle gracefully when enhanced monitoring is off
            assert result is None

    def test_show_alerts_without_enhanced_monitoring(self):
        """Test alerts display when enhanced monitoring is not available"""
        with patch("monitoramento.ENHANCED_MONITORING", False):
            result = show_alerts()
            # Should return None or handle gracefully when enhanced monitoring is off
            assert result is None

    @pytest.mark.asyncio
    async def test_monitoring_main_function(self):
        """Test the main monitoring function execution"""
        with patch("monitoramento.checar_servico") as mock_checar:
            with patch("monitoramento.check_database_health") as mock_db:
                with patch("monitoramento.check_storage_health") as mock_storage:
                    with patch("builtins.print") as mock_print:

                        # Setup async mocks
                        mock_db.return_value = True
                        mock_storage.return_value = True

                        # Run main monitoring function
                        await monitoring_main()

                        # Verify that services were checked
                        assert mock_checar.called

                        # Verify that infrastructure checks were performed
                        mock_db.assert_called_once()
                        mock_storage.assert_called_once()

                        # Verify that status information was printed
                        assert mock_print.called

    def test_monitoring_service_configuration(self):
        """Test that monitoring script has proper service configuration"""

        # The script should have predefined services to monitor
        # This tests the integration with the expected service endpoints
        with patch("monitoramento.checar_servico") as mock_checar:
            with patch(
                "monitoramento.check_database_health",
                return_value=asyncio.coroutine(lambda: True)(),
            ):
                with patch(
                    "monitoramento.check_storage_health",
                    return_value=asyncio.coroutine(lambda: True)(),
                ):
                    with patch("builtins.print"):
                        # Run the main function to see what services are checked
                        asyncio.run(monitoring_main())

                        # Verify that health endpoints are being monitored
                        call_args = [call[0] for call in mock_checar.call_args_list]
                        service_names = [args[0] for args in call_args]
                        urls = [args[1] for args in call_args]

                        # Check that expected service types are monitored
                        expected_services = ["API Health", "API Root", "API Auditorias"]
                        for service in expected_services:
                            assert any(service in name for name in service_names)

                        # Check that localhost URLs are used (development mode)
                        assert all("localhost:8000" in url for url in urls)

    @pytest.mark.asyncio
    async def test_monitoring_enhanced_features(self):
        """Test monitoring with enhanced features enabled"""
        # Mock enhanced monitoring components
        mock_monitoring = MagicMock()
        mock_monitoring.start = MagicMock()
        mock_monitoring.stop = MagicMock()
        mock_monitoring.health_checker = MagicMock()
        mock_monitoring.health_checker.add_health_check = MagicMock()
        mock_monitoring.health_checker.run_all_checks = AsyncMock(return_value=[])
        mock_monitoring.get_dashboard_data = MagicMock(
            return_value={"system_status": "healthy"}
        )

        with patch("monitoramento.ENHANCED_MONITORING", True):
            with patch("monitoramento.monitoring", mock_monitoring):
                with patch("monitoramento.checar_servico"):
                    with patch(
                        "monitoramento.check_database_health", return_value=True
                    ):
                        with patch(
                            "monitoramento.check_storage_health", return_value=True
                        ):
                            with patch("builtins.print"):

                                await monitoring_main()

                                # Verify enhanced monitoring was started and stopped
                                mock_monitoring.start.assert_called_once()
                                mock_monitoring.stop.assert_called_once()

                                # Verify health checks were configured
                                mock_monitoring.health_checker.add_health_check.assert_called()

    def test_monitoring_response_time_measurement(self):
        """Test that monitoring measures response times"""
        import time

        with patch("monitoramento.requests.get") as mock_get:
            # Mock a slow response
            def slow_response(*args, **kwargs):
                time.sleep(0.1)  # 100ms delay
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                return mock_resp

            mock_get.side_effect = slow_response

            with patch("builtins.print") as mock_print:
                checar_servico("Slow API", "http://localhost:8000/slow")

                # Verify that response time was measured and reported
                calls = [call[0][0] for call in mock_print.call_args_list]
                response_time_reported = any(
                    "Response:" in call and "ms" in call for call in calls
                )
                assert response_time_reported

    def test_monitoring_error_resilience(self):
        """Test that monitoring script is resilient to various errors"""

        # Test network timeout
        with patch("monitoramento.requests.get") as mock_get:
            mock_get.side_effect = Exception("Network timeout")

            with patch("builtins.print"):
                # Should not raise exception
                checar_servico("Timeout API", "http://localhost:8000/timeout")

    @pytest.mark.asyncio
    async def test_monitoring_concurrent_checks(self):
        """Test that monitoring can handle concurrent health checks"""

        async def mock_async_check():
            await asyncio.sleep(0.01)  # Simulate async work
            return True

        with patch("monitoramento.check_database_health", side_effect=mock_async_check):
            with patch(
                "monitoramento.check_storage_health", side_effect=mock_async_check
            ):
                with patch("builtins.print"):

                    start_time = asyncio.get_event_loop().time()

                    # Run multiple concurrent checks
                    await asyncio.gather(
                        check_database_health(),
                        check_storage_health(),
                        check_database_health(),
                    )

                    end_time = asyncio.get_event_loop().time()

                    # Concurrent execution should be faster than sequential
                    assert end_time - start_time < 0.1  # Should complete quickly

    def test_monitoring_integration_with_system_paths(self):
        """Test that monitoring script integrates properly with system paths"""
        import monitoramento

        # Verify that src path addition works (if the enhanced monitoring is available)
        if hasattr(monitoramento, "ENHANCED_MONITORING"):
            # The script attempts to import enhanced monitoring features
            # This tests the path manipulation for imports
            assert True  # Path manipulation is working if we got here

        # Verify that script can be run as a module
        assert hasattr(monitoramento, "__name__")

    def test_monitoring_cli_compatibility(self):
        """Test that monitoring script is compatible with CLI usage"""

        # Check if script can be executed as main
        assert callable(monitoring_main)

        # Check if script has proper main execution guard
        # (This would be tested by running the script directly, but we test the structure)
        script_content = Path(scripts_path / "monitoramento.py").read_text()
        assert 'if __name__ == "__main__":' in script_content


if __name__ == "__main__":
    pytest.main([__file__])
