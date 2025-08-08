#!/usr/bin/env python3
"""
AUDITORIA360 - Production Configuration Audit Runner
====================================================

This script helps validate the multi-tenant production configuration
by running comprehensive audit checks on the database schema, security
policies, and data integrity.

Usage:
    python scripts/audit/run_production_audit.py [--help]
    
Requirements:
    - Supabase connection configured
    - psycopg2 or psycopg2-binary installed
    - Environment variables for database connection
"""

import os
import sys
import glob
from pathlib import Path
from typing import List, Dict, Any
import logging

# Add the project root to the path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductionAuditRunner:
    """Runs production audit validation scripts for AUDITORIA360."""
    
    def __init__(self, audit_scripts_dir: str = None):
        """Initialize the audit runner.
        
        Args:
            audit_scripts_dir: Directory containing audit SQL scripts
        """
        if audit_scripts_dir is None:
            audit_scripts_dir = Path(__file__).parent
        
        self.audit_scripts_dir = Path(audit_scripts_dir)
        self.scripts = self._load_audit_scripts()
        
    def _load_audit_scripts(self) -> Dict[str, str]:
        """Load all SQL audit scripts from the directory."""
        scripts = {}
        
        # Load individual scripts
        script_files = sorted(glob.glob(str(self.audit_scripts_dir / "*.sql")))
        
        for script_file in script_files:
            script_name = Path(script_file).stem
            try:
                with open(script_file, 'r', encoding='utf-8') as f:
                    scripts[script_name] = f.read()
                logger.info(f"Loaded audit script: {script_name}")
            except Exception as e:
                logger.error(f"Error loading script {script_file}: {e}")
                
        return scripts
    
    def validate_sql_syntax(self) -> bool:
        """Basic validation of SQL syntax in scripts."""
        logger.info("🔍 Validating SQL syntax in audit scripts...")
        
        validation_errors = []
        
        for script_name, sql_content in self.scripts.items():
            # Basic syntax checks
            if not sql_content.strip():
                validation_errors.append(f"{script_name}: Empty script")
                continue
                
            # Check for basic SQL keywords
            sql_upper = sql_content.upper()
            if not any(keyword in sql_upper for keyword in ['SELECT', 'FROM', 'WHERE']):
                validation_errors.append(f"{script_name}: No SQL queries found")
                continue
                
            # Check for proper statement termination
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]
            if not statements:
                validation_errors.append(f"{script_name}: No valid SQL statements found")
                continue
                
            logger.info(f"✅ {script_name}: {len(statements)} SQL statements found")
        
        if validation_errors:
            logger.error("❌ SQL validation errors found:")
            for error in validation_errors:
                logger.error(f"  - {error}")
            return False
        
        logger.info("✅ All SQL audit scripts passed basic syntax validation")
        return True
    
    def list_audit_scripts(self) -> None:
        """List all available audit scripts."""
        logger.info("📋 Available audit scripts:")
        
        for script_name in sorted(self.scripts.keys()):
            script_path = self.audit_scripts_dir / f"{script_name}.sql"
            logger.info(f"  - {script_name} ({script_path})")
    
    def get_audit_instructions(self) -> str:
        """Get formatted instructions for running the audit."""
        instructions = """
🔍 AUDITORIA360 - Production Configuration Audit Instructions
============================================================

To run the complete production audit, follow these steps:

1. 📝 Access your Supabase SQL Editor
   - Go to your Supabase project dashboard
   - Navigate to SQL Editor

2. 🎯 Option A: Run Complete Audit (Recommended)
   - Copy and paste the content of: scripts/audit/complete_production_audit.sql
   - Execute the entire script
   - Review all results systematically

3. 🔍 Option B: Run Individual Scripts
   - Execute scripts in numerical order (01 through 07):
"""
        
        # Add individual script list
        individual_scripts = [
            ("01_schema_validation.sql", "Verify main tables exist"),
            ("02_columns_relationships_validation.sql", "Verify multi-tenant columns"),
            ("03_rls_status_validation.sql", "Check RLS status"),
            ("04_security_policies_validation.sql", "List security policies"),
            ("05_contabilidades_validation.sql", "Verify accounting firms"),
            ("06_users_contabilidades_relationship_validation.sql", "Check user-accounting relationships"),
            ("07_empresas_contabilidades_relationship_validation.sql", "Check company-accounting relationships")
        ]
        
        for script_name, description in individual_scripts:
            instructions += f"     - {script_name}: {description}\n"
        
        instructions += """
4. 📊 Expected Results Summary:
   - All tables should exist (tabela_existe = true)
   - All sensitive tables should have RLS enabled (rls_ativada = true)
   - All users should have contabilidade_id assigned
   - No "orphan" companies without contabilidade_id
   - Security policies should be present and correctly configured

5. 🚨 Critical Failure Points:
   - Users without contabilidade_id: RLS will NOT work
   - Tables without RLS: Data isolation compromised
   - Missing security policies: Data access blocked
   - Orphan companies: Data integrity issues

6. 🔧 If Issues Found:
   - Run the migration: migrations/006_unified_multi_tenant_security.sql
   - Assign users to accounting firms in the profiles table
   - Enable RLS on sensitive tables
   - Create missing security policies

✅ Success Criteria:
If all scripts run successfully with expected results, your AUDITORIA360
platform is correctly configured for secure multi-tenant production operation.

For detailed documentation, see: scripts/audit/README.md
"""
        
        return instructions

def main():
    """Main entry point for the audit runner."""
    print("🔍 AUDITORIA360 - Production Configuration Audit Runner")
    print("=" * 60)
    
    # Initialize the audit runner
    try:
        runner = ProductionAuditRunner()
    except Exception as e:
        logger.error(f"Failed to initialize audit runner: {e}")
        sys.exit(1)
    
    # List available scripts
    runner.list_audit_scripts()
    print()
    
    # Validate SQL syntax
    if not runner.validate_sql_syntax():
        logger.error("❌ SQL validation failed. Please fix syntax errors before proceeding.")
        sys.exit(1)
    
    print()
    
    # Show instructions
    print(runner.get_audit_instructions())
    
    print("\n" + "=" * 60)
    print("🎉 Audit runner completed successfully!")
    print("📝 Follow the instructions above to run the production audit in Supabase.")
    

if __name__ == "__main__":
    main()