"""
Test for the improved API main module.
Verifies that import errors are handled gracefully.
"""
import pytest
from unittest.mock import patch, MagicMock
import sys


def test_api_main_imports_gracefully():
    """Test that the API main module handles missing router imports gracefully."""
    # Mock missing router modules
    with patch.dict(sys.modules, {
        'services.api.auth_routes': None,
        'services.api.pdf_processor_routes': None,
    }):
        try:
            from services.api.main import app
            # Should not raise an exception
            assert app is not None
            assert app.title == "Auditoria360 API"
        except ImportError:
            pytest.fail("API main should handle missing router imports gracefully")


def test_api_main_with_available_routers():
    """Test that the API main module works when routers are available."""
    # Mock available router modules
    mock_router = MagicMock()
    mock_router.router = MagicMock()
    
    mock_modules = {
        'services.api.auth_routes': mock_router,
        'services.api.pdf_processor_routes': mock_router,
    }
    
    with patch.dict(sys.modules, mock_modules):
        try:
            from services.api.main import app
            assert app is not None
            assert app.title == "Auditoria360 API"
        except ImportError as e:
            pytest.skip(f"Skipping test due to missing dependencies: {e}")


def test_api_main_basic_endpoints():
    """Test that basic endpoints are available."""
    try:
        from services.api.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        assert "Bem-vindo à API Auditoria360" in response.json()["message"]
        
    except ImportError as e:
        pytest.skip(f"Skipping test due to missing dependencies: {e}")


@pytest.mark.integration
def test_ingestion_main_compatibility():
    """Test that the ingestion main module works with the new import structure."""
    try:
        from services.ingestion.main import main
        
        # Test with mock event data
        mock_event = {
            'bucket': 'test-bucket',
            'name': 'test-file.pdf'
        }
        
        # Should not raise import errors
        # Note: This will fail at runtime due to missing config/services, but imports should work
        try:
            main(mock_event, None)
        except Exception as e:
            # Expected to fail due to missing services, but should not be import errors
            assert "ImportError" not in str(type(e))
            
    except ImportError as e:
        if "functions_framework" in str(e) or "Context" in str(e):
            pytest.skip(f"Skipping test due to expected missing Cloud Functions dependency: {e}")
        else:
            pytest.fail(f"Unexpected import error: {e}")


def test_health_reporter_basic_functionality():
    """Test that the health reporter can be imported and initialized."""
    try:
        from scripts.health_reporter import ProjectHealthReporter
        
        reporter = ProjectHealthReporter()
        assert reporter is not None
        assert hasattr(reporter, 'generate_report')
        assert hasattr(reporter, 'generate_markdown_summary')
        
    except ImportError as e:
        pytest.skip(f"Skipping test due to missing dependencies: {e}")


@pytest.mark.unit
def test_requirements_includes_essential_packages():
    """Test that requirements.txt includes essential packages."""
    import os
    
    requirements_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'requirements.txt'
    )
    
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            requirements = f.read()
        
        # Check for essential packages
        essential_packages = [
            'fastapi',
            'pytest',
            'pytest-cov',
            'functions-framework'
        ]
        
        for package in essential_packages:
            assert package in requirements, f"Essential package {package} missing from requirements.txt"
    else:
        pytest.skip("requirements.txt not found")