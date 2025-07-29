"""
Tests for the modular backend structure
Validates that the core, services, and utils modules are properly organized
"""

import pytest
import sys
import os

def test_core_module_imports():
    """Test that core module components can be imported."""
    try:
        from src.core import validate_cpf, setup_logging
        from src.core import DataValidator, get_logger
        # Import ConfigManager separately to handle initialization
        from src.core.config_manager import ConfigManager
        assert True, "Core module imports successful"
    except ImportError as e:
        pytest.fail(f"Failed to import core module components: {e}")

def test_services_module_imports():
    """Test that services module components can be imported.""" 
    try:
        from src.services import auth_service, cache_service, payroll_service
        assert True, "Services module imports successful"
    except ImportError as e:
        pytest.fail(f"Failed to import services module components: {e}")

def test_utils_module_imports():
    """Test that utils module components can be imported."""
    try:
        from src.utils import get_monitoring_system, profile, cached
        assert True, "Utils module imports successful"
    except ImportError as e:
        pytest.fail(f"Failed to import utils module components: {e}")

def test_core_validators_functionality():
    """Test core validation functions work correctly."""
    from src.core import validate_cpf, validate_cnpj, validate_email, DataValidator
    
    # Test CPF validation
    assert validate_cpf("11144477735") == True  # Valid CPF
    assert validate_cpf("12345678901") == False  # Invalid CPF
    assert validate_cpf("111.444.777-35") == True  # Valid CPF with formatting
    
    # Test CNPJ validation  
    assert validate_cnpj("11222333000181") == True  # Valid CNPJ
    assert validate_cnpj("12345678000100") == False  # Invalid CNPJ
    
    # Test email validation
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    
    # Test DataValidator class
    validator = DataValidator()
    assert validator.validate_cpf("11144477735") == True
    assert validator.validate_email("test@example.com") == True

def test_core_logging_functionality():
    """Test core logging functions work correctly."""
    from src.core import setup_logging, get_logger
    
    logger = setup_logging()
    assert logger is not None
    
    app_logger = get_logger("test_app")
    assert app_logger is not None
    assert app_logger.name == "test_app"

def test_module_structure():
    """Test that the expected module structure exists."""
    import os
    
    # Check core module structure
    assert os.path.exists("src/core/__init__.py")
    assert os.path.exists("src/core/config_manager.py")
    assert os.path.exists("src/core/validators.py")
    assert os.path.exists("src/core/log_utils.py")
    assert os.path.exists("src/core/README.md")
    
    # Check services module structure
    assert os.path.exists("src/services/__init__.py")
    assert os.path.exists("src/services/auth_service.py")
    
    # Check utils module structure  
    assert os.path.exists("src/utils/__init__.py")
    assert os.path.exists("src/utils/monitoring.py")

def test_config_manager_functionality():
    """Test ConfigManager can be instantiated."""
    from src.core.config_manager import ConfigManager
    
    # Test that the class can be imported and instantiated
    config_manager = ConfigManager()
    assert config_manager is not None
    assert hasattr(config_manager, 'config')

if __name__ == "__main__":
    pytest.main([__file__, "-v"])