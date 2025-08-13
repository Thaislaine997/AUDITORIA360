#!/usr/bin/env python3
"""
IAI-C Validation Test Suite
===========================
Part of the Manifesto da Singularidade Serverless

This test suite validates that the IAI-C (Intrinsic Artificial Intelligence in Code)
system correctly detects semantic violations and business logic errors.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, expect_failure: bool = False) -> tuple[bool, str]:
    """Run a command and return success status and output"""
    try:
        # The command should be run from the project root
        result = subprocess.run(cmd, capture_output=True, text=True)

        success = (
            (result.returncode == 0) if not expect_failure else (result.returncode != 0)
        )
        output = result.stdout + result.stderr

        return success, output
    except Exception as e:
        return False, str(e)


def test_semantic_intent_validator():
    """Test that semantic intent validator detects business logic violations"""
    print("🧠 Testing IAI-C Semantic Intent Validator...")

    # Test on payroll service which has intentional violations
    success, output = run_command(
        [
            "python",
            "scripts/python/semantic_intent_validator.py",
            "src/services/payroll_service.py",
        ]
    )

    # Should detect warnings (not critical, but violations)
    if (
        "semantic warnings detected" in output.lower()
        or "missing_validation" in output.lower()
    ):
        print("✅ Semantic Intent Validator correctly detected business logic issues")
        return True
    else:
        print("❌ Semantic Intent Validator failed to detect known issues")
        print(f"Output: {output}")
        return False


def test_business_logic_validator():
    """Test that business logic validator detects critical violations"""
    print("💼 Testing IAI-C Business Logic Validator...")

    # Test should detect the intentional vacation calculation violation
    success, output = run_command(
        [
            "python",
            "scripts/python/business_logic_validator.py",
            "src/services/payroll_service.py",
        ],
        expect_failure=True,
    )

    if success and (
        "negative_validation" in output
        or "vacation function lacks protection" in output
    ):
        print("✅ Business Logic Validator correctly detected critical violation")
        return True
    else:
        print("❌ Business Logic Validator failed to detect intentional violation")
        print(f"Output: {output}")
        return False


def test_dependency_entropy_scanner():
    """Test that dependency entropy scanner identifies unused dependencies"""
    print("🧬 Testing IAI-C Dependency Entropy Scanner...")

    # Should detect unused dependencies and exit with error code
    success, output = run_command(
        ["python", "scripts/python/dependency_entropy_scanner.py"], expect_failure=True
    )

    if success and "high entropy dependencies detected" in output.lower():
        print("✅ Dependency Entropy Scanner correctly identified unused dependencies")
        return True
    else:
        print("❌ Dependency Entropy Scanner failed to identify entropy issues")
        print(f"Output: {output}")
        return False


def test_health_monitor_integration():
    """Test the complete health monitoring system"""
    print("🔧 Testing IAI-C Health Monitor Integration...")

    # Run the health monitor script
    success, output = run_command(["./scripts/shell/iai_c_health_monitor.sh"])

    if "IAI-C Monitoring Complete" in output:
        print("✅ Health Monitor completed successfully")
        return True
    else:
        print("❌ Health Monitor failed to complete")
        print(f"Output: {output}")
        return False


def validate_iai_c_requirements():
    """Validate that all IAI-C requirements from the manifesto are met"""
    print("\n🎯 Validating IAI-C Manifesto Requirements...")

    requirements = {
        "Semantic Intent Detection": False,
        "Business Logic Validation": False,
        "Dependency Entropy Analysis": False,
        "Pre-commit Integration": False,
        "CI/CD Semantic Analysis": False,
        "Edge Resilience Configuration": False,
        "Zero-Cost Architecture": False,
    }

    # Check pre-commit config
    precommit_path = Path(".pre-commit-config.yaml")
    if precommit_path.exists():
        with open(precommit_path, "r") as f:
            content = f.read()
            if "semantic-intent-validator" in content:
                requirements["Pre-commit Integration"] = True

    # Check CI/CD workflow
    workflow_path = Path(".github") / "workflows" / "ci-cd.yml"
    if workflow_path.exists():
        with open(workflow_path, "r") as f:
            content = f.read()
            if "IAI-C Semantic Intent Analysis" in content:
                requirements["CI/CD Semantic Analysis"] = True

    # Check Vercel config for edge resilience
    vercel_path = Path("vercel.json")
    if vercel_path.exists():
        with open(vercel_path, "r") as f:
            content = f.read()
            if "regions" in content and "Cache-Control" in content:
                requirements["Edge Resilience Configuration"] = True
                requirements["Zero-Cost Architecture"] = True  # Vercel = serverless

    # Run individual tests
    if test_semantic_intent_validator():
        requirements["Semantic Intent Detection"] = True

    if test_business_logic_validator():
        requirements["Business Logic Validation"] = True

    if test_dependency_entropy_scanner():
        requirements["Dependency Entropy Analysis"] = True

    # Report results
    print("\n📊 IAI-C Requirements Validation Results:")
    print("=" * 50)

    all_passed = True
    for requirement, passed in requirements.items():
        status = "✅" if passed else "❌"
        print(f"{status} {requirement}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("🎉 ALL IAI-C REQUIREMENTS MET!")
        print("🧬 The digital organism has achieved consciousness.")
        print("🌟 Manifesto da Singularidade Serverless: IMPLEMENTED")
        return True
    else:
        failed_count = sum(1 for passed in requirements.values() if not passed)
        print(f"⚠️  {failed_count} requirements not yet met.")
        print("🔧 Continue development to achieve full consciousness.")
        return False


def main():
    """Main test runner"""
    print("🧬 IAI-C System Validation Test Suite")
    print("=====================================")
    print("Validating the Manifesto da Singularidade Serverless implementation...\n")

    try:
        # Ensure we're in the project root
        script_dir = Path(__file__).parent  # scripts/python
        project_root = script_dir.parent.parent  # go up two levels
        os.chdir(project_root)

        print(f"Working directory: {os.getcwd()}")

        # Run validation
        success = validate_iai_c_requirements()

        # Test health monitor as final integration test
        print("\n🔧 Final Integration Test:")
        if test_health_monitor_integration():
            print("✅ Integration test passed")
        else:
            success = False
            print("❌ Integration test failed")

        print("\n" + "=" * 50)
        if success:
            print("🌟 IAI-C SYSTEM FULLY OPERATIONAL")
            print("🧬 The conscious serverless organism is alive!")
            sys.exit(0)
        else:
            print("⚠️  IAI-C SYSTEM NEEDS ATTENTION")
            print("🔧 Some components require further development")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
