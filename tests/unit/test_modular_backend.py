"""
Test for the modular backend structure.
Validates that the new modular organization works correctly.
"""

import unittest
from unittest.mock import patch, MagicMock


class TestModularBackend(unittest.TestCase):
    """Test cases for the modular backend structure."""

    def test_core_imports(self):
        """Test that core modules can be imported correctly."""
        try:
            from src.core import ConfigManager
            from src.core.exceptions import AuditoriaException, ValidationError
            from src.core.validators import validate_cpf, validate_email
            
            self.assertTrue(callable(ConfigManager))
            self.assertTrue(issubclass(AuditoriaException, Exception))
            self.assertTrue(issubclass(ValidationError, AuditoriaException))
            self.assertTrue(callable(validate_cpf))
            self.assertTrue(callable(validate_email))
            
        except ImportError as e:
            self.fail(f"Failed to import core modules: {e}")

    def test_services_imports(self):
        """Test that service modules can be imported correctly."""
        try:
            from src.services.ocr import OCRService
            from src.services.storage import StorageService
            
            self.assertTrue(callable(OCRService))
            self.assertTrue(callable(StorageService))
            
        except ImportError as e:
            self.fail(f"Failed to import service modules: {e}")

    def test_utils_imports(self):
        """Test that utility modules can be imported correctly."""
        try:
            from src.utils import MonitoringSystem, PerformanceProfiler
            
            self.assertTrue(callable(MonitoringSystem))
            self.assertTrue(callable(PerformanceProfiler))
            
        except ImportError as e:
            self.fail(f"Failed to import utility modules: {e}")

    def test_config_manager_functionality(self):
        """Test ConfigManager basic functionality."""
        from src.core.config import ConfigManager
        
        config_manager = ConfigManager()
        
        # Test basic config operations
        config_manager.update_config({"test_key": "test_value"})
        self.assertEqual(config_manager.get("test_key"), "test_value")
        self.assertEqual(config_manager.get("nonexistent_key", "default"), "default")

    def test_validators_functionality(self):
        """Test validator functions."""
        from src.core.validators import validate_cpf, validate_email, validate_required_fields
        from src.core.exceptions import ValidationError
        
        # Test CPF validation
        self.assertFalse(validate_cpf(""))
        self.assertFalse(validate_cpf("123"))
        self.assertFalse(validate_cpf("11111111111"))  # All same digits
        
        # Test email validation  
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email(""))
        
        # Test required fields validation
        with self.assertRaises(ValidationError):
            validate_required_fields({}, ["required_field"])
        
        with self.assertRaises(ValidationError):
            validate_required_fields({"field": ""}, ["field"])

    @patch('src.services.ocr.ocr_service.PaddleOCR')
    def test_ocr_service_functionality(self, mock_paddle_ocr):
        """Test OCR service basic functionality."""
        from src.services.ocr import OCRService
        
        # Mock PaddleOCR
        mock_ocr_instance = MagicMock()
        mock_paddle_ocr.return_value = mock_ocr_instance
        mock_ocr_instance.ocr.return_value = [[
            [None, ["Texto de teste", 0.95]]
        ]]
        
        ocr_service = OCRService()
        result = ocr_service.extract_text("test_file.pdf")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["extracted_text"], "Texto de teste")
        self.assertEqual(result["confidence"], 0.95)

    def test_legacy_compatibility(self):
        """Test that legacy functions still work for backward compatibility."""
        try:
            # Test that main functions still work as before
            from src.main import process_document_ocr, process_control_sheet
            
            result1 = process_document_ocr("test.pdf", "test-bucket")
            self.assertEqual(result1["status"], "success")
            self.assertIn("extracted_text", result1)
            
            result2 = process_control_sheet("test.xlsx", "test-bucket")
            self.assertEqual(result2["status"], "success")
            self.assertIn("rows_processed", result2)
            
        except Exception as e:
            self.fail(f"Legacy compatibility broken: {e}")

    def test_modular_structure_isolation(self):
        """Test that modules are properly isolated and don't have circular dependencies."""
        import importlib
        import sys
        
        # Test that we can import each module independently
        modules_to_test = [
            'src.core.config',
            'src.core.exceptions', 
            'src.core.validators',
            'src.core.security',
        ]
        
        for module_name in modules_to_test:
            try:
                # Remove from cache if already imported
                if module_name in sys.modules:
                    del sys.modules[module_name]
                
                module = importlib.import_module(module_name)
                self.assertIsNotNone(module)
                
            except ImportError as e:
                self.fail(f"Module {module_name} has import issues: {e}")


if __name__ == '__main__':
    unittest.main()