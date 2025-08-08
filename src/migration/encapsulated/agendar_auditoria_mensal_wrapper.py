#!/usr/bin/env python3
"""
Security Wrapper for Legacy Script: scripts/batch/agendar_auditoria_mensal.bat
Generated on: 2025-08-06T19:19:03.179349
Security issues detected: []
"""

import hashlib
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SecurityWrapper:
    """Security wrapper for legacy script execution"""

    def __init__(self):
        self.original_script = Path("scripts/batch/agendar_auditoria_mensal.bat")
        self.script_hash = self._calculate_script_hash()
        self.max_execution_time = 300  # 5 minutes timeout

    def _calculate_script_hash(self):
        """Calculate hash of original script for integrity check"""
        if self.original_script.exists():
            with open(self.original_script, "rb") as f:
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
        security_issues = []
        if security_issues:
            logger.warning(f"⚠️ Security issues detected: {security_issues}")

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

        logger.info(f"🚀 Executing legacy script: {self.original_script}")

        try:
            # Log execution start
            self._log_execution_start()

            # Execute with timeout and monitoring
            if self.original_script.suffix == ".ps1":
                result = subprocess.run(
                    [
                        "powershell",
                        "-ExecutionPolicy",
                        "Restricted",
                        "-File",
                        str(self.original_script),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=self.max_execution_time,
                )
            elif self.original_script.suffix == ".bat":
                result = subprocess.run(
                    [str(self.original_script)],
                    capture_output=True,
                    text=True,
                    timeout=self.max_execution_time,
                )
            else:
                logger.error("❌ Unsupported script type")
                return 1

            # Log execution results
            self._log_execution_result(result)

            return result.returncode

        except subprocess.TimeoutExpired:
            logger.error(
                f"❌ Script execution timeout after {self.max_execution_time} seconds"
            )
            return 124
        except Exception as e:
            logger.error(f"❌ Script execution failed: {e}")
            return 1

    def _log_execution_start(self):
        """Log execution start for audit trail"""
        audit_log = {
            "timestamp": datetime.now().isoformat(),
            "script": str(self.original_script),
            "action": "execution_start",
            "security_issues": [],
            "user": os.getenv("USER", "unknown"),
        }

        audit_file = Path("logs/legacy_script_audit.json")
        audit_file.parent.mkdir(exist_ok=True)

        with open(audit_file, "a") as f:
            f.write(json.dumps(audit_log) + "\n")

    def _log_execution_result(self, result):
        """Log execution results for audit trail"""
        audit_log = {
            "timestamp": datetime.now().isoformat(),
            "script": str(self.original_script),
            "action": "execution_complete",
            "return_code": result.returncode,
            "stdout_length": len(result.stdout),
            "stderr_length": len(result.stderr),
            "success": result.returncode == 0,
        }

        audit_file = Path("logs/legacy_script_audit.json")
        with open(audit_file, "a") as f:
            f.write(json.dumps(audit_log) + "\n")


def main():
    """Main execution function"""
    wrapper = SecurityWrapper()
    return wrapper.execute_with_monitoring()


if __name__ == "__main__":
    sys.exit(main())
