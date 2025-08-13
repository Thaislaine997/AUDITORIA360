#!/usr/bin/env python3
"""
AUDITORIA360 Workflow Validation Tests
Tests to ensure all implemented workflows are correctly configured.
"""

import os
import yaml
import json
import pytest
from pathlib import Path

# Constants
WORKFLOWS_DIR = Path(".github/workflows")
EXPECTED_WORKFLOWS = [
    "auto-checklist.yml",
    "e2e.yml", 
    "codeql-analysis.yml",
    "changelog.yml",
    "check-docs.yml",
    "notify-slack.yml",
    "export-logs.yml"
]

def test_workflows_directory_exists():
    """Test that workflows directory exists"""
    assert WORKFLOWS_DIR.exists(), "Workflows directory should exist"

def test_all_expected_workflows_exist():
    """Test that all expected workflows are present"""
    existing_workflows = [f.name for f in WORKFLOWS_DIR.glob("*.yml")]
    
    for expected_workflow in EXPECTED_WORKFLOWS:
        assert expected_workflow in existing_workflows, f"Workflow {expected_workflow} should exist"

def test_workflow_yaml_validity():
    """Test that all workflow files are valid YAML"""
    for workflow_file in WORKFLOWS_DIR.glob("*.yml"):
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Workflow {workflow_file.name} is not valid YAML: {e}")

def test_workflow_basic_structure():
    """Test that workflows have required basic structure"""
    for workflow_file in WORKFLOWS_DIR.glob("*.yml"):
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow = yaml.safe_load(f)
            
        # Basic structure checks
        assert 'name' in workflow, f"Workflow {workflow_file.name} should have a name"
        assert 'on' in workflow, f"Workflow {workflow_file.name} should have triggers"
        assert 'jobs' in workflow, f"Workflow {workflow_file.name} should have jobs"

def test_auto_checklist_workflow():
    """Test auto-checklist workflow configuration"""
    workflow_path = WORKFLOWS_DIR / "auto-checklist.yml"
    assert workflow_path.exists(), "Auto-checklist workflow should exist"
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)
    
    # Check schedule is configured
    assert 'schedule' in workflow['on'], "Auto-checklist should have schedule trigger"
    # Check manual trigger
    assert 'workflow_dispatch' in workflow['on'], "Auto-checklist should have manual trigger"

def test_e2e_workflow():
    """Test E2E workflow configuration"""
    workflow_path = WORKFLOWS_DIR / "e2e.yml"
    assert workflow_path.exists(), "E2E workflow should exist"
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)
    
    # Check push and PR triggers
    assert 'push' in workflow['on'], "E2E should trigger on push"
    assert 'pull_request' in workflow['on'], "E2E should trigger on PR"

def test_codeql_workflow():
    """Test CodeQL workflow configuration"""
    workflow_path = WORKFLOWS_DIR / "codeql-analysis.yml"
    assert workflow_path.exists(), "CodeQL workflow should exist"
    
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)
    
    # Check required permissions
    jobs = workflow['jobs']
    analyze_job = jobs.get('analyze', {})
    permissions = analyze_job.get('permissions', {})
    
    assert 'security-events' in permissions, "CodeQL should have security-events permission"

def test_dependabot_configuration():
    """Test Dependabot configuration"""
    dependabot_path = Path(".github/dependabot.yml")
    assert dependabot_path.exists(), "Dependabot configuration should exist"
    
    with open(dependabot_path, 'r', encoding='utf-8') as f:
        dependabot = yaml.safe_load(f)
    
    assert dependabot['version'] == 2, "Dependabot should use version 2"
    assert 'updates' in dependabot, "Dependabot should have updates configuration"
    
    # Check for Python and GitHub Actions ecosystems
    ecosystems = [update['package-ecosystem'] for update in dependabot['updates']]
    assert 'pip' in ecosystems, "Dependabot should monitor Python packages"
    assert 'github-actions' in ecosystems, "Dependabot should monitor GitHub Actions"

def test_setup_script_exists():
    """Test that setup script exists and is executable"""
    setup_script = Path("setup_local.sh")
    assert setup_script.exists(), "Setup script should exist"
    
    # Check if it's executable (on Unix systems)
    if os.name != 'nt':  # Not Windows
        assert os.access(setup_script, os.X_OK), "Setup script should be executable"

def test_readme_has_workflow_badges():
    """Test that README has workflow status badges"""
    readme_path = Path("README.md")
    assert readme_path.exists(), "README should exist"
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Check for GitHub Actions badge patterns
    assert "actions/workflows/" in readme_content, "README should have workflow badges"
    assert "badge.svg" in readme_content, "README should have SVG badges"

def test_manual_supremo_updated():
    """Test that MANUAL_SUPREMO.md has been updated with implementation status"""
    manual_path = Path("MANUAL_SUPREMO.md")
    assert manual_path.exists(), "MANUAL_SUPREMO should exist"
    
    with open(manual_path, 'r', encoding='utf-8') as f:
        manual_content = f.read()
    
    # Check for implementation status section
    assert "STATUS DA IMPLEMENTAÇÃO SUPREMA" in manual_content, "Manual should have implementation status"
    assert "Automações Implementadas" in manual_content, "Manual should list implemented automations"

def test_workflow_artifact_upload():
    """Test that workflows properly upload artifacts"""
    critical_workflows = [
        "auto-checklist.yml",
        "e2e.yml",
        "export-logs.yml"
    ]
    
    for workflow_name in critical_workflows:
        workflow_path = WORKFLOWS_DIR / workflow_name
        with open(workflow_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "upload-artifact" in content, f"Workflow {workflow_name} should upload artifacts"

def test_workflow_error_handling():
    """Test that workflows have proper error handling"""
    for workflow_file in WORKFLOWS_DIR.glob("*.yml"):
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for common error handling patterns
        if "continue-on-error" in content or "if: always()" in content:
            # This workflow has some error handling
            continue
        else:
            # At least basic validation should exist
            assert "checkout@v" in content, f"Workflow {workflow_file.name} should use proper action versions"

if __name__ == "__main__":
    # Run tests if executed directly
    import sys
    
    print("🧪 AUDITORIA360 Workflow Validation Tests")
    print("=" * 50)
    
    # Change to repository root if needed
    if not Path(".github").exists():
        print("❌ Please run this from the repository root directory")
        sys.exit(1)
    
    # Simple test runner
    test_functions = [
        test_workflows_directory_exists,
        test_all_expected_workflows_exist,
        test_workflow_yaml_validity,
        test_workflow_basic_structure,
        test_auto_checklist_workflow,
        test_e2e_workflow,
        test_codeql_workflow,
        test_dependabot_configuration,
        test_setup_script_exists,
        test_readme_has_workflow_badges,
        test_manual_supremo_updated,
        test_workflow_artifact_upload,
        test_workflow_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✅ {test_func.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All workflow validation tests passed!")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed - please review the configuration")
        sys.exit(1)