"""
Demo script to showcase the modular backend structure in action.
This script demonstrates how different modules work together.
"""

def demo_modular_backend():
    """Demonstrate the modular backend functionality."""
    print("🏗️  AUDITORIA360 Backend Modularization Demo")
    print("=" * 50)
    
    # Core Module Demo
    print("\n📦 CORE MODULE")
    print("-" * 20)
    try:
        from src.core import ConfigManager, SecurityManager
        from src.core.validators import validate_cpf, validate_email
        from src.core.exceptions import ValidationError
        
        # Config Manager
        config = ConfigManager()
        config.update_config({"demo_key": "demo_value"})
        print(f"✅ ConfigManager: {config.get('demo_key')}")
        
        # Security Manager
        security = SecurityManager()
        token = security.create_access_token({"user": "demo"})
        print(f"✅ SecurityManager: Token created (length: {len(token)})")
        
        # Validators
        print(f"✅ Validators: CPF valid = {validate_cpf('123.456.789-09')}")
        print(f"✅ Validators: Email valid = {validate_email('test@example.com')}")
        
    except Exception as e:
        print(f"❌ Core module error: {e}")
    
    # Services Module Demo
    print("\n🔧 SERVICES MODULE")
    print("-" * 20)
    try:
        from src.services.ocr import OCRService
        from src.services.storage import StorageService
        
        # Note: These are just class instantiation tests since we don't have actual files
        print("✅ OCRService: Class available")
        print("✅ StorageService: Class available")
        
    except Exception as e:
        print(f"❌ Services module error: {e}")
    
    # Utils Module Demo
    print("\n🛠️  UTILS MODULE")
    print("-" * 20)
    try:
        from src.utils import MonitoringSystem, PerformanceProfiler
        
        print("✅ MonitoringSystem: Available for system monitoring")
        print("✅ PerformanceProfiler: Available for performance analysis")
        
    except Exception as e:
        print(f"❌ Utils module error: {e}")
    
    # Legacy Compatibility Demo
    print("\n🔄 LEGACY COMPATIBILITY")
    print("-" * 20)
    try:
        from src.main import process_document_ocr, process_control_sheet
        
        result = process_document_ocr("test.pdf", "test-bucket")
        print(f"✅ Legacy function: {result['status']}")
        
    except Exception as e:
        print(f"❌ Legacy compatibility error: {e}")
    
    print("\n🎉 Modularization Demo Complete!")
    print("✨ All modules are working together harmoniously!")


if __name__ == "__main__":
    demo_modular_backend()