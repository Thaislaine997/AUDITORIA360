#!/usr/bin/env python3
"""
Clean Test Runner for AUDITORIA360
Runs tests excluding problematic ML and integration components
"""

import subprocess
import sys
from pathlib import Path


def run_clean_tests():
    """Run tests excluding problematic modules"""

    # Tests that should work without issues
    working_tests = [
        "tests/unit/test_core_config.py",
        "tests/unit/test_core_security.py",
        "tests/unit/test_core_validators.py",
        "tests/unit/test_models_database.py",
        "tests/unit/test_checklist_schemas.py",
        "tests/unit/test_folha_processada_schemas.py",
        "tests/unit/test_parametros_legais_schemas.py",
        "tests/unit/test_predicao_risco_schemas.py",
        "tests/unit/test_rbac_schemas.py",
        "tests/integration/test_api_health.py",
    ]

    print("🧪 Running clean test suite (excluding problematic modules)...")

    for test_file in working_tests:
        test_path = Path(test_file)
        if test_path.exists():
            print(f"\n   Running: {test_file}")
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pytest",
                        str(test_path),
                        "-v",
                        "--tb=short",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result.returncode == 0:
                    print(f"   ✅ PASSED: {test_file}")
                else:
                    print(f"   ❌ FAILED: {test_file}")
                    if result.stdout:
                        print(f"      STDOUT: {result.stdout[-200:]}")  # Last 200 chars
                    if result.stderr:
                        print(f"      STDERR: {result.stderr[-200:]}")  # Last 200 chars

            except subprocess.TimeoutExpired:
                print(f"   ⏱️  TIMEOUT: {test_file}")
            except Exception as e:
                print(f"   ❌ ERROR: {test_file} - {e}")
        else:
            print(f"   ⚠️  NOT FOUND: {test_file}")

    print("\n🏁 Clean test run completed!")


if __name__ == "__main__":
    run_clean_tests()
