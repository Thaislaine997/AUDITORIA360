#!/usr/bin/env python3
"""
Basic test script to verify improvements without external dependencies.
Tests structural improvements and import handling.
"""

import sys
import os
import traceback
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_api_main_resilience():
    """Test that API main handles missing imports gracefully."""
    print("Testing API main import resilience...")
    
    # Mock missing modules
    with patch.dict(sys.modules, {
        'fastapi': MagicMock(),
        'fastapi.middleware.cors': MagicMock(),
    }):
        try:
            from services.api.main import app
            print("✅ API main imports successfully with mocked dependencies")
            return True
        except Exception as e:
            print(f"❌ API main import failed: {e}")
            traceback.print_exc()
            return False

def test_ingestion_main_resilience():
    """Test that ingestion main handles missing imports gracefully."""
    print("Testing ingestion main import resilience...")
    
    # Mock missing modules
    with patch.dict(sys.modules, {
        'google.cloud.bigquery': MagicMock(),
        'google.cloud.documentai': MagicMock(),
        'google.cloud.storage': MagicMock(),
        'google.auth': MagicMock(),
        'functions_framework': MagicMock(),
    }):
        try:
            from services.ingestion.main import main
            print("✅ Ingestion main imports successfully with mocked dependencies")
            return True
        except Exception as e:
            print(f"❌ Ingestion main import failed: {e}")
            traceback.print_exc()
            return False

def test_health_reporter():
    """Test that health reporter imports and initializes."""
    print("Testing health reporter...")
    try:
        from scripts.health_reporter import ProjectHealthReporter
        reporter = ProjectHealthReporter()
        print("✅ Health reporter imports and initializes successfully")
        return True
    except Exception as e:
        print(f"❌ Health reporter failed: {e}")
        traceback.print_exc()
        return False

def test_requirements_file():
    """Test that requirements.txt has been updated."""
    print("Testing requirements.txt updates...")
    try:
        requirements_path = os.path.join(project_root, 'requirements.txt')
        with open(requirements_path, 'r') as f:
            content = f.read()
        
        essential_packages = ['pytest', 'pytest-cov', 'functions-framework']
        missing = []
        
        for package in essential_packages:
            if package not in content:
                missing.append(package)
        
        if missing:
            print(f"❌ Missing packages in requirements.txt: {missing}")
            return False
        else:
            print("✅ Requirements.txt includes essential packages")
            return True
            
    except Exception as e:
        print(f"❌ Failed to check requirements.txt: {e}")
        return False

def test_ci_workflow():
    """Test that CI workflow has been updated."""
    print("Testing CI workflow updates...")
    try:
        ci_path = os.path.join(project_root, '.github', 'workflows', 'ci.yml')
        with open(ci_path, 'r') as f:
            content = f.read()
        
        improvements = [
            'lint-and-security',
            'dependency-check',
            'matrix:',
            'safety',
            'bandit'
        ]
        
        missing = []
        for improvement in improvements:
            if improvement not in content:
                missing.append(improvement)
        
        if missing:
            print(f"❌ Missing improvements in CI workflow: {missing}")
            return False
        else:
            print("✅ CI workflow includes security and quality checks")
            return True
            
    except Exception as e:
        print(f"❌ Failed to check CI workflow: {e}")
        return False

def test_weekly_report_workflow():
    """Test that weekly report workflow exists."""
    print("Testing weekly report workflow...")
    try:
        report_path = os.path.join(project_root, '.github', 'workflows', 'weekly-report.yml')
        if os.path.exists(report_path):
            print("✅ Weekly report workflow created")
            return True
        else:
            print("❌ Weekly report workflow missing")
            return False
    except Exception as e:
        print(f"❌ Failed to check weekly report workflow: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("AUDITORIA360 Improvements Verification")
    print("="*60)
    
    tests = [
        test_api_main_resilience,
        test_ingestion_main_resilience,
        test_health_reporter,
        test_requirements_file,
        test_ci_workflow,
        test_weekly_report_workflow,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All improvements verified successfully!")
        return 0
    else:
        print("⚠️  Some improvements need attention")
        return 1

if __name__ == '__main__':
    sys.exit(main())