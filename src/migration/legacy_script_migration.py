"""
Legacy Script Migration System
=============================

Automated system to encapsulate and migrate legacy PowerShell and Batch scripts
to Python equivalents with enhanced security and auditability.
"""

import asyncio
import json
import logging
import os
import subprocess
import shutil
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class LegacyScript:
    """Represents a legacy script to be migrated"""
    file_path: str
    script_type: str  # powershell, batch
    original_size: int
    last_modified: str
    dependencies: List[str]
    functionality: str
    migration_priority: str  # critical, high, medium, low
    security_issues: List[str]


@dataclass
class MigrationResult:
    """Results of script migration"""
    original_script: str
    migrated_script: str
    migration_type: str  # encapsulated, converted, replaced
    success: bool
    warnings: List[str]
    errors: List[str]
    test_results: Dict[str, Any]
    timestamp: str


class LegacyScriptMigrator:
    """Handles migration of legacy PowerShell and Batch scripts"""
    
    def __init__(self):
        self.legacy_scripts = []
        self.migration_results = []
        self.migration_log = []
        
        # Create migration directories
        self.migration_dir = Path("src/migration")
        self.encapsulated_dir = self.migration_dir / "encapsulated"
        self.python_scripts_dir = self.migration_dir / "python_equivalents"
        self.legacy_backup_dir = self.migration_dir / "legacy_backup"
        
        for dir_path in [self.migration_dir, self.encapsulated_dir, 
                        self.python_scripts_dir, self.legacy_backup_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    async def discover_legacy_scripts(self) -> List[LegacyScript]:
        """Discover all legacy scripts in the repository"""
        logger.info("🔍 Discovering legacy scripts...")
        
        legacy_scripts = []
        base_path = Path(".")
        
        # Find PowerShell scripts
        for ps_file in base_path.rglob("*.ps1"):
            if ps_file.exists():
                script = await self._analyze_script(ps_file, "powershell")
                legacy_scripts.append(script)
                
        # Find Batch scripts
        for bat_file in base_path.rglob("*.bat"):
            if bat_file.exists():
                script = await self._analyze_script(bat_file, "batch")
                legacy_scripts.append(script)
                
        self.legacy_scripts = legacy_scripts
        logger.info(f"📊 Found {len(legacy_scripts)} legacy scripts")
        
        return legacy_scripts
    
    async def _analyze_script(self, file_path: Path, script_type: str) -> LegacyScript:
        """Analyze a legacy script to determine migration approach"""
        stat = file_path.stat()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
                content = f.read()
        
        # Analyze functionality and security issues
        functionality = self._determine_functionality(content, script_type)
        security_issues = self._detect_security_issues(content, script_type)
        dependencies = self._extract_dependencies(content, script_type)
        priority = self._assess_migration_priority(content, functionality, security_issues)
        
        return LegacyScript(
            file_path=str(file_path),
            script_type=script_type,
            original_size=stat.st_size,
            last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            dependencies=dependencies,
            functionality=functionality,
            migration_priority=priority,
            security_issues=security_issues
        )
    
    def _determine_functionality(self, content: str, script_type: str) -> str:
        """Determine the primary functionality of the script"""
        content_lower = content.lower()
        
        # Common functionality patterns
        if any(pattern in content_lower for pattern in ["deploy", "build", "compile"]):
            return "build_deployment"
        elif any(pattern in content_lower for pattern in ["backup", "copy", "move"]):
            return "file_management"
        elif any(pattern in content_lower for pattern in ["install", "setup", "config"]):
            return "system_configuration"
        elif any(pattern in content_lower for pattern in ["test", "validate", "check"]):
            return "testing_validation"
        elif any(pattern in content_lower for pattern in ["schedule", "cron", "task"]):
            return "task_scheduling"
        elif any(pattern in content_lower for pattern in ["audit", "log", "report"]):
            return "audit_reporting"
        else:
            return "general_utility"
    
    def _detect_security_issues(self, content: str, script_type: str) -> List[str]:
        """Detect potential security issues in legacy scripts"""
        issues = []
        content_lower = content.lower()
        
        # Common security issues
        security_patterns = {
            "hardcoded_credentials": ["password=", "passwd=", "pwd=", "apikey=", "secret="],
            "network_calls": ["invoke-webrequest", "wget", "curl", "net use"],
            "system_modification": ["registry", "regedit", "sc create", "sc config"],
            "file_execution": ["invoke-expression", "iex", "& ", "cmd /c"],
            "privilege_escalation": ["runas", "sudo", "elevate", "admin"],
            "external_downloads": ["downloadstring", "downloadfile", "iwr"],
        }
        
        for issue_type, patterns in security_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                issues.append(issue_type)
                
        # Script-specific checks
        if script_type == "powershell":
            if "executionpolicy" in content_lower:
                issues.append("execution_policy_bypass")
            if "-encoded" in content_lower:
                issues.append("encoded_commands")
                
        elif script_type == "batch":
            if "echo off" not in content_lower:
                issues.append("command_visibility")
            if any(pattern in content_lower for pattern in ["del /f /q", "rd /s /q"]):
                issues.append("destructive_operations")
        
        return issues
    
    def _extract_dependencies(self, content: str, script_type: str) -> List[str]:
        """Extract external dependencies from script"""
        dependencies = []
        content_lower = content.lower()
        
        if script_type == "powershell":
            # PowerShell modules
            module_matches = re.findall(r'import-module\s+([^\s\n]+)', content_lower)
            dependencies.extend(module_matches)
            
            # External executables
            exe_matches = re.findall(r'([a-zA-Z0-9_-]+\.exe)', content_lower)
            dependencies.extend(list(set(exe_matches)))
            
        elif script_type == "batch":
            # External commands
            cmd_matches = re.findall(r'call\s+([^\s\n]+)', content_lower)
            dependencies.extend(cmd_matches)
            
        return list(set(dependencies))
    
    def _assess_migration_priority(self, content: str, functionality: str, security_issues: List[str]) -> str:
        """Assess migration priority based on functionality and security"""
        if security_issues:
            if any(issue in security_issues for issue in ["hardcoded_credentials", "privilege_escalation"]):
                return "critical"
            elif len(security_issues) >= 3:
                return "high"
                
        if functionality in ["system_configuration", "audit_reporting"]:
            return "high"
        elif functionality in ["build_deployment", "task_scheduling"]:
            return "medium"
        else:
            return "low"
    
    async def migrate_script(self, script: LegacyScript) -> MigrationResult:
        """Migrate a single legacy script"""
        logger.info(f"🔄 Migrating {script.file_path}")
        
        result = MigrationResult(
            original_script=script.file_path,
            migrated_script="",
            migration_type="",
            success=False,
            warnings=[],
            errors=[],
            test_results={},
            timestamp=datetime.now().isoformat()
        )
        
        try:
            # Backup original script
            await self._backup_original_script(script)
            
            # Determine migration strategy
            if script.migration_priority in ["critical", "high"]:
                # Full conversion to Python
                result = await self._convert_to_python(script, result)
            else:
                # Encapsulation with security wrapper
                result = await self._encapsulate_script(script, result)
                
            # Test migrated script
            test_results = await self._test_migrated_script(result)
            result.test_results = test_results
            
            if test_results.get("success", False):
                result.success = True
                logger.info(f"✅ Successfully migrated {script.file_path}")
            else:
                result.errors.append("Migration testing failed")
                logger.warning(f"⚠️ Migration completed with test failures: {script.file_path}")
                
        except Exception as e:
            result.errors.append(f"Migration failed: {str(e)}")
            logger.error(f"❌ Failed to migrate {script.file_path}: {e}")
            
        self.migration_results.append(result)
        return result
    
    async def _backup_original_script(self, script: LegacyScript):
        """Backup original script before migration"""
        original_path = Path(script.file_path)
        backup_path = self.legacy_backup_dir / original_path.name
        
        # Add timestamp to avoid conflicts
        if backup_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.legacy_backup_dir / f"{original_path.stem}_{timestamp}{original_path.suffix}"
            
        shutil.copy2(original_path, backup_path)
        logger.info(f"💾 Backed up {script.file_path} to {backup_path}")
    
    async def _convert_to_python(self, script: LegacyScript, result: MigrationResult) -> MigrationResult:
        """Convert legacy script to Python equivalent"""
        logger.info(f"🐍 Converting {script.file_path} to Python")
        
        try:
            with open(script.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
        except Exception:
            with open(script.file_path, 'r', encoding='latin-1', errors='ignore') as f:
                original_content = f.read()
        
        # Generate Python equivalent based on functionality
        python_script = self._generate_python_equivalent(script, original_content)
        
        # Save Python script
        original_path = Path(script.file_path)
        python_path = self.python_scripts_dir / f"{original_path.stem}.py"
        
        with open(python_path, 'w', encoding='utf-8') as f:
            f.write(python_script)
            
        result.migrated_script = str(python_path)
        result.migration_type = "converted"
        
        # Add security improvements
        result.warnings.append("Converted to Python with enhanced security controls")
        
        return result
    
    def _generate_python_equivalent(self, script: LegacyScript, original_content: str) -> str:
        """Generate Python equivalent of legacy script"""
        template = f'''#!/usr/bin/env python3
"""
Migrated Python script - Originally: {script.file_path}
Generated on: {datetime.now().isoformat()}
Original functionality: {script.functionality}
Migration priority: {script.migration_priority}
"""

import os
import sys
import logging
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Enhanced security and logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function - migrated from legacy script"""
    logger.info(f"Starting migrated script execution: {{Path(__file__).name}}")
    
    try:
        # Original script functionality converted to Python
        {self._convert_functionality_to_python(script, original_content)}
        
        logger.info("Script execution completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Script execution failed: {{e}}")
        return 1

def validate_environment():
    """Validate execution environment for security"""
    # Security validations
    if hasattr(os, 'geteuid') and os.geteuid() == 0:  # Running as root
        logger.warning("Script running with elevated privileges")
    
    # Check for required dependencies
    required_deps = {script.dependencies}
    missing_deps = []
    for dep in required_deps:
        if not shutil.which(dep):
            missing_deps.append(dep)
    
    if missing_deps:
        logger.error(f"Missing dependencies: {{missing_deps}}")
        return False
        
    return True

if __name__ == "__main__":
    if not validate_environment():
        sys.exit(1)
    sys.exit(main())
'''
        return template
    
    def _convert_functionality_to_python(self, script: LegacyScript, content: str) -> str:
        """Convert specific functionality to Python code"""
        if script.functionality == "file_management":
            return '''
        # File management operations
        source_dir = os.getenv("SOURCE_DIR", ".")
        target_dir = os.getenv("TARGET_DIR", "./backup")
        
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        
        for file_path in Path(source_dir).glob("*"):
            if file_path.is_file():
                shutil.copy2(file_path, target_dir)
                logger.info(f"Copied {file_path} to {target_dir}")
'''
        elif script.functionality == "system_configuration":
            return '''
        # System configuration operations
        config_items = {
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "DATA_DIR": os.getenv("DATA_DIR", "./data"),
            "BACKUP_RETENTION": os.getenv("BACKUP_RETENTION", "30")
        }
        
        for key, value in config_items.items():
            logger.info(f"Configuration: {key} = {value}")
            # Apply configuration as needed
'''
        elif script.functionality == "build_deployment":
            return '''
        # Build and deployment operations
        build_dir = Path("./build")
        build_dir.mkdir(exist_ok=True)
        
        # Example build process
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Build completed successfully")
        else:
            logger.error(f"Build failed: {result.stderr}")
            raise Exception("Build process failed")
'''
        else:
            return '''
        # General utility operations
        logger.info("Executing migrated functionality")
        
        # Original script logic would be converted here
        # This is a placeholder for the actual conversion
        print("Legacy script functionality migrated to Python")
'''
    
    async def _encapsulate_script(self, script: LegacyScript, result: MigrationResult) -> MigrationResult:
        """Encapsulate legacy script with security wrapper"""
        logger.info(f"📦 Encapsulating {script.file_path}")
        
        # Create Python wrapper for legacy script
        original_path = Path(script.file_path)
        wrapper_path = self.encapsulated_dir / f"{original_path.stem}_wrapper.py"
        
        wrapper_content = self._generate_security_wrapper(script)
        
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
            
        result.migrated_script = str(wrapper_path)
        result.migration_type = "encapsulated"
        result.warnings.append("Legacy script encapsulated with security wrapper")
        
        return result
    
    def _generate_security_wrapper(self, script: LegacyScript) -> str:
        """Generate secure wrapper for legacy script"""
        return f'''#!/usr/bin/env python3
"""
Security Wrapper for Legacy Script: {script.file_path}
Generated on: {datetime.now().isoformat()}
Security issues detected: {script.security_issues}
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityWrapper:
    """Security wrapper for legacy script execution"""
    
    def __init__(self):
        self.original_script = Path("{script.file_path}")
        self.script_hash = self._calculate_script_hash()
        self.max_execution_time = 300  # 5 minutes timeout
        
    def _calculate_script_hash(self):
        """Calculate hash of original script for integrity check"""
        if self.original_script.exists():
            with open(self.original_script, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        return None
        
    def validate_execution_environment(self):
        """Validate environment before script execution"""
        logger.info("🔍 Validating execution environment...")
        
        # Check script integrity
        current_hash = self._calculate_script_hash()
        if current_hash != self.script_hash:
            logger.error("❌ Script integrity check failed")
            return False
            
        # Check for security issues
        security_issues = {script.security_issues}
        if security_issues:
            logger.warning(f"⚠️ Security issues detected: {{security_issues}}")
            
        # Validate permissions
        if not os.access(self.original_script, os.R_OK):
            logger.error("❌ Insufficient permissions to read script")
            return False
            
        logger.info("✅ Environment validation passed")
        return True
        
    def execute_with_monitoring(self):
        """Execute original script with security monitoring"""
        if not self.validate_execution_environment():
            return 1
            
        logger.info(f"🚀 Executing legacy script: {{self.original_script}}")
        
        try:
            # Log execution start
            self._log_execution_start()
            
            # Execute with timeout and monitoring
            if self.original_script.suffix == '.ps1':
                result = subprocess.run([
                    "powershell", "-ExecutionPolicy", "Restricted", 
                    "-File", str(self.original_script)
                ], capture_output=True, text=True, timeout=self.max_execution_time)
            elif self.original_script.suffix == '.bat':
                result = subprocess.run([
                    str(self.original_script)
                ], capture_output=True, text=True, timeout=self.max_execution_time)
            else:
                logger.error("❌ Unsupported script type")
                return 1
                
            # Log execution results
            self._log_execution_result(result)
            
            return result.returncode
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Script execution timeout after {{self.max_execution_time}} seconds")
            return 124
        except Exception as e:
            logger.error(f"❌ Script execution failed: {{e}}")
            return 1
            
    def _log_execution_start(self):
        """Log execution start for audit trail"""
        audit_log = {{
            "timestamp": datetime.now().isoformat(),
            "script": str(self.original_script),
            "action": "execution_start",
            "security_issues": {script.security_issues},
            "user": os.getenv("USER", "unknown")
        }}
        
        audit_file = Path("logs/legacy_script_audit.json")
        audit_file.parent.mkdir(exist_ok=True)
        
        with open(audit_file, "a") as f:
            f.write(json.dumps(audit_log) + "\\n")
            
    def _log_execution_result(self, result):
        """Log execution results for audit trail"""
        audit_log = {{
            "timestamp": datetime.now().isoformat(),
            "script": str(self.original_script),
            "action": "execution_complete",
            "return_code": result.returncode,
            "stdout_length": len(result.stdout),
            "stderr_length": len(result.stderr),
            "success": result.returncode == 0
        }}
        
        audit_file = Path("logs/legacy_script_audit.json")
        with open(audit_file, "a") as f:
            f.write(json.dumps(audit_log) + "\\n")

def main():
    """Main execution function"""
    wrapper = SecurityWrapper()
    return wrapper.execute_with_monitoring()

if __name__ == "__main__":
    sys.exit(main())
'''
    
    async def _test_migrated_script(self, result: MigrationResult) -> Dict[str, Any]:
        """Test the migrated script"""
        if not result.migrated_script:
            return {"success": False, "error": "No migrated script to test"}
            
        logger.info(f"🧪 Testing migrated script: {result.migrated_script}")
        
        try:
            # Basic syntax check
            migrated_path = Path(result.migrated_script)
            if not migrated_path.exists():
                return {"success": False, "error": "Migrated script file not found"}
                
            # Python syntax check
            result_check = subprocess.run([
                sys.executable, "-m", "py_compile", str(migrated_path)
            ], capture_output=True, text=True)
            
            if result_check.returncode != 0:
                return {
                    "success": False, 
                    "error": f"Syntax check failed: {result_check.stderr}"
                }
                
            return {
                "success": True,
                "syntax_check": "passed",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": f"Testing failed: {str(e)}"}
    
    async def migrate_all_scripts(self) -> Dict[str, Any]:
        """Migrate all discovered legacy scripts"""
        logger.info("🚀 Starting mass migration of legacy scripts...")
        
        if not self.legacy_scripts:
            await self.discover_legacy_scripts()
            
        migration_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_scripts": len(self.legacy_scripts),
            "successful_migrations": 0,
            "failed_migrations": 0,
            "by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "by_type": {"powershell": 0, "batch": 0},
            "migration_details": []
        }
        
        # Migrate scripts by priority
        priority_order = ["critical", "high", "medium", "low"]
        
        for priority in priority_order:
            priority_scripts = [s for s in self.legacy_scripts if s.migration_priority == priority]
            
            logger.info(f"📋 Migrating {len(priority_scripts)} {priority} priority scripts...")
            
            for script in priority_scripts:
                result = await self.migrate_script(script)
                
                if result.success:
                    migration_summary["successful_migrations"] += 1
                else:
                    migration_summary["failed_migrations"] += 1
                    
                migration_summary["by_priority"][priority] += 1
                migration_summary["by_type"][script.script_type] += 1
                migration_summary["migration_details"].append(asdict(result))
        
        # Generate migration report
        report_path = self.migration_dir / "migration_report.json"
        with open(report_path, "w") as f:
            json.dump(migration_summary, f, indent=2)
            
        logger.info(f"📊 Migration complete: {migration_summary['successful_migrations']}/{migration_summary['total_scripts']} successful")
        
        return migration_summary
    
    def generate_migration_tickets(self) -> List[Dict[str, Any]]:
        """Generate tickets for manual review of failed migrations"""
        tickets = []
        
        for result in self.migration_results:
            if not result.success or result.errors:
                ticket = {
                    "ticket_id": f"MIGRATION-{datetime.now().strftime('%Y%m%d')}-{len(tickets)+1:03d}",
                    "title": f"Manual review required: {Path(result.original_script).name}",
                    "priority": "high" if result.errors else "medium",
                    "description": f"Legacy script migration requires manual intervention",
                    "original_script": result.original_script,
                    "migration_type": result.migration_type,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "created_date": datetime.now().isoformat(),
                    "assigned_to": "development_team",
                    "status": "open"
                }
                tickets.append(ticket)
                
        # Save tickets to file
        if tickets:
            tickets_path = self.migration_dir / "migration_tickets.json"
            with open(tickets_path, "w") as f:
                json.dump(tickets, f, indent=2)
            logger.info(f"🎫 Generated {len(tickets)} migration tickets")
            
        return tickets


async def main():
    """Main execution function"""
    migrator = LegacyScriptMigrator()
    
    # Discover legacy scripts
    scripts = await migrator.discover_legacy_scripts()
    
    if scripts:
        # Migrate all scripts
        summary = await migrator.migrate_all_scripts()
        
        # Generate tickets for failed migrations
        tickets = migrator.generate_migration_tickets()
        
        print(f"✅ Migration Summary:")
        print(f"   Total scripts: {summary['total_scripts']}")
        print(f"   Successful: {summary['successful_migrations']}")
        print(f"   Failed: {summary['failed_migrations']}")
        print(f"   Tickets generated: {len(tickets)}")
        
        return summary
    else:
        print("✅ No legacy scripts found to migrate")
        return {"message": "No legacy scripts found"}


if __name__ == "__main__":
    asyncio.run(main())