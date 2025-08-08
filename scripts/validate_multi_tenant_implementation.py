#!/usr/bin/env python3
"""
Test script to validate the multi-tenant migration implementation
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_migration_script_syntax():
    """Test that the migration script compiles correctly"""
    try:
        migration_script = project_root / "scripts" / "migracao.py"
        with open(migration_script, 'r') as f:
            code = f.read()
        
        compile(code, str(migration_script), 'exec')
        logger.info("✅ Migration script syntax is valid")
        return True
    except Exception as e:
        logger.error(f"❌ Migration script syntax error: {e}")
        return False

def test_sql_script_exists():
    """Test that the SQL script exists and is readable"""
    try:
        sql_script = project_root / "migrations" / "006_unified_multi_tenant_security.sql"
        if not sql_script.exists():
            logger.error(f"❌ SQL script not found: {sql_script}")
            return False
        
        with open(sql_script, 'r') as f:
            content = f.read()
        
        # Basic validation - check for key elements
        required_elements = [
            'CREATE TABLE IF NOT EXISTS public."Contabilidades"',
            'CREATE TABLE IF NOT EXISTS public.profiles',
            'ALTER TABLE public."Empresas"',
            'ENABLE ROW LEVEL SECURITY',
            'CREATE OR REPLACE FUNCTION auth.get_contabilidade_id()'
        ]
        
        for element in required_elements:
            if element not in content:
                logger.error(f"❌ Missing required SQL element: {element}")
                return False
        
        logger.info("✅ SQL script contains all required elements")
        return True
    except Exception as e:
        logger.error(f"❌ SQL script validation error: {e}")
        return False

def test_documentation_exists():
    """Test that documentation files exist"""
    try:
        doc_file = project_root / "docs" / "MULTI_TENANT_IMPLEMENTATION_GUIDE.md"
        if not doc_file.exists():
            logger.error(f"❌ Documentation not found: {doc_file}")
            return False
        
        logger.info("✅ Documentation exists")
        return True
    except Exception as e:
        logger.error(f"❌ Documentation validation error: {e}")
        return False

def test_environment_template_exists():
    """Test that environment template exists"""
    try:
        env_template = project_root / ".env.multi-tenant-template"
        if not env_template.exists():
            logger.error(f"❌ Environment template not found: {env_template}")
            return False
        
        with open(env_template, 'r') as f:
            content = f.read()
        
        # Check for required environment variables
        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_SERVICE_KEY'
        ]
        
        for var in required_vars:
            if var not in content:
                logger.error(f"❌ Missing required environment variable: {var}")
                return False
        
        logger.info("✅ Environment template is valid")
        return True
    except Exception as e:
        logger.error(f"❌ Environment template validation error: {e}")
        return False

def test_requirements_file_exists():
    """Test that migration requirements file exists"""
    try:
        req_file = project_root / "scripts" / "requirements-migration.txt"
        if not req_file.exists():
            logger.error(f"❌ Migration requirements not found: {req_file}")
            return False
        
        with open(req_file, 'r') as f:
            content = f.read()
        
        # Check for required packages
        required_packages = [
            'pdfplumber',
            'pandas',
            'supabase',
            'python-dotenv'
        ]
        
        for package in required_packages:
            if package not in content:
                logger.error(f"❌ Missing required package: {package}")
                return False
        
        logger.info("✅ Migration requirements file is valid")
        return True
    except Exception as e:
        logger.error(f"❌ Migration requirements validation error: {e}")
        return False

def main():
    """Run all validation tests"""
    logger.info("🚀 Running Multi-Tenant Implementation Validation Tests")
    
    tests = [
        test_migration_script_syntax,
        test_sql_script_exists,
        test_documentation_exists,
        test_environment_template_exists,
        test_requirements_file_exists
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    logger.info(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All validation tests passed! Multi-tenant implementation is ready.")
        return 0
    else:
        logger.error("❌ Some validation tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())