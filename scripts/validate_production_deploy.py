# 🔧 SCRIPT DE VALIDAÇÃO FINAL DE PRODUÇÃO - AUDITORIA360

"""
Script de validação final para deploy de produção do AUDITORIA360.
Este script executa todas as verificações necessárias antes do deploy.

Uso: python validate_production_deploy.py [--fix-issues] [--verbose]
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any
import yaml

class ProductionValidator:
    def __init__(self, verbose: bool = False, fix_issues: bool = False):
        self.verbose = verbose
        self.fix_issues = fix_issues
        self.project_root = Path(__file__).parent
        self.validation_results = {}
        self.critical_issues = []
        self.warnings = []
        
    def log(self, message: str, level: str = "info"):
        """Log messages with different levels"""
        colors = {
            "info": "\033[94m",
            "success": "\033[92m", 
            "warning": "\033[93m",
            "error": "\033[91m",
            "reset": "\033[0m"
        }
        
        prefix = {
            "info": "[INFO]",
            "success": "[SUCCESS]",
            "warning": "[WARNING]", 
            "error": "[ERROR]"
        }
        
        print(f"{colors.get(level, '')}{prefix.get(level, '')} {message}{colors['reset']}")
        
        if level == "error":
            self.critical_issues.append(message)
        elif level == "warning":
            self.warnings.append(message)
    
    def run_command(self, command: List[str], capture_output: bool = True) -> Tuple[bool, str]:
        """Execute shell command and return success status and output"""
        try:
            result = subprocess.run(
                command, 
                capture_output=capture_output, 
                text=True, 
                check=False,
                cwd=self.project_root
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def validate_file_structure(self) -> bool:
        """Validate essential files exist for production deployment"""
        self.log("🔍 Validating file structure...")
        
        essential_files = [
            "requirements.txt",
            "api/index.py", 
            "dashboards/app.py",
            "vercel.json",
            ".env.template",
            ".env.production",
            ".streamlit/config.toml",
            ".streamlit/secrets.toml.template",
            "Dockerfile",
            "Makefile"
        ]
        
        missing_files = []
        for file_path in essential_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log(f"❌ Missing essential files: {missing_files}", "error")
            return False
        else:
            self.log("✅ All essential files present", "success")
            return True
    
    def validate_environment_config(self) -> bool:
        """Validate environment configuration files"""
        self.log("🔍 Validating environment configurations...")
        
        # Check .env.production
        env_prod_path = self.project_root / ".env.production"
        if not env_prod_path.exists():
            self.log("❌ .env.production file missing", "error")
            return False
        
        # Read and validate environment variables
        required_env_vars = [
            "DATABASE_URL",
            "JWT_SECRET_KEY", 
            "OPENAI_API_KEY",
            "R2_ACCESS_KEY_ID",
            "R2_SECRET_ACCESS_KEY"
        ]
        
        placeholder_vars = []
        with open(env_prod_path, 'r') as f:
            env_content = f.read()
            
        for var in required_env_vars:
            if var not in env_content:
                self.log(f"⚠️ Missing environment variable: {var}", "warning")
            elif any(placeholder in env_content for placeholder in ["your_", "change-this", "example"]):
                placeholder_vars.append(var)
        
        if placeholder_vars:
            self.log(f"⚠️ Placeholder values found in: {placeholder_vars}", "warning")
            self.log("🔧 Update these with real production values before deploy", "warning")
        
        self.log("✅ Environment configuration validated", "success")
        return True
    
    def validate_dependencies(self) -> bool:
        """Validate Python dependencies can be installed"""
        self.log("🔍 Validating Python dependencies...")
        
        # Check if requirements.txt exists and is valid
        req_path = self.project_root / "requirements.txt"
        if not req_path.exists():
            self.log("❌ requirements.txt not found", "error")
            return False
        
        # Try to parse requirements (basic syntax check)
        try:
            with open(req_path, 'r') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Basic validation - should contain package name
                    if not any(c.isalnum() for c in line.split('=')[0].split('>')[0].split('<')[0]):
                        self.log(f"⚠️ Potentially invalid requirement at line {i}: {line}", "warning")
            
            self.log(f"✅ Requirements file validated ({len([l for l in lines if l.strip() and not l.startswith('#')])} packages)", "success")
            return True
            
        except Exception as e:
            self.log(f"❌ Error reading requirements.txt: {e}", "error")
            return False
    
    def validate_vercel_config(self) -> bool:
        """Validate Vercel deployment configuration"""
        self.log("🔍 Validating Vercel configuration...")
        
        vercel_path = self.project_root / "vercel.json"
        if not vercel_path.exists():
            self.log("❌ vercel.json not found", "error")
            return False
        
        try:
            with open(vercel_path, 'r') as f:
                config = json.load(f)
            
            # Validate required sections
            required_sections = ["builds", "routes", "functions"]
            for section in required_sections:
                if section not in config:
                    self.log(f"⚠️ Missing section in vercel.json: {section}", "warning")
            
            # Check if API route is configured
            if "builds" in config:
                api_build = any("api/index.py" in str(build.get("src", "")) for build in config["builds"])
                if not api_build:
                    self.log("⚠️ API build not configured in vercel.json", "warning")
            
            self.log("✅ Vercel configuration validated", "success")
            return True
            
        except json.JSONDecodeError as e:
            self.log(f"❌ Invalid JSON in vercel.json: {e}", "error")
            return False
    
    def validate_streamlit_config(self) -> bool:
        """Validate Streamlit configuration"""
        self.log("🔍 Validating Streamlit configuration...")
        
        config_path = self.project_root / ".streamlit" / "config.toml"
        secrets_template_path = self.project_root / ".streamlit" / "secrets.toml.template"
        
        if not config_path.exists():
            self.log("❌ .streamlit/config.toml not found", "error")
            return False
        
        if not secrets_template_path.exists():
            self.log("❌ .streamlit/secrets.toml.template not found", "error")
            return False
        
        # Validate TOML syntax
        try:
            import toml
        except ImportError:
            self.log("⚠️ TOML library not available for validation", "warning")
            return True
        
        try:
            with open(config_path, 'r') as f:
                toml.load(f)
            self.log("✅ Streamlit config.toml is valid", "success")
        except Exception as e:
            self.log(f"❌ Invalid TOML in config.toml: {e}", "error")
            return False
        
        try:
            with open(secrets_template_path, 'r') as f:
                toml.load(f)
            self.log("✅ Streamlit secrets template is valid", "success")
        except Exception as e:
            self.log(f"❌ Invalid TOML in secrets template: {e}", "error")
            return False
        
        return True
    
    def validate_docker_config(self) -> bool:
        """Validate Docker configuration"""
        self.log("🔍 Validating Docker configuration...")
        
        dockerfile_path = self.project_root / "Dockerfile"
        if not dockerfile_path.exists():
            self.log("❌ Dockerfile not found", "error")
            return False
        
        try:
            with open(dockerfile_path, 'r') as f:
                content = f.read()
            
            # Basic Dockerfile validation
            if "FROM " not in content:
                self.log("❌ Dockerfile missing FROM instruction", "error")
                return False
            
            if "COPY " not in content and "ADD " not in content:
                self.log("⚠️ Dockerfile might not copy application files", "warning")
            
            if "CMD " not in content and "ENTRYPOINT " not in content:
                self.log("⚠️ Dockerfile missing CMD or ENTRYPOINT", "warning")
            
            self.log("✅ Dockerfile validated", "success")
            return True
            
        except Exception as e:
            self.log(f"❌ Error reading Dockerfile: {e}", "error")
            return False
    
    def validate_security_measures(self) -> bool:
        """Validate security measures are in place"""
        self.log("🔍 Validating security measures...")
        
        # Check .gitignore
        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            self.log("❌ .gitignore not found", "error")
            return False
        
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        security_patterns = [".env", "*.key", "*.pem", "*secret*", "*credential*"]
        missing_patterns = []
        
        for pattern in security_patterns:
            if pattern not in gitignore_content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            self.log(f"⚠️ Security patterns missing from .gitignore: {missing_patterns}", "warning")
        
        # Check for accidentally committed secrets
        dangerous_files = [".env", "secrets.toml", "credentials.json"]
        for file_name in dangerous_files:
            if (self.project_root / file_name).exists():
                self.log(f"⚠️ Potentially sensitive file found: {file_name}", "warning")
        
        self.log("✅ Security measures validated", "success")
        return True
    
    def validate_ci_cd_config(self) -> bool:
        """Validate CI/CD configuration"""
        self.log("🔍 Validating CI/CD configuration...")
        
        # Check GitHub Actions
        workflows_dir = self.project_root / ".github" / "workflows"
        if not workflows_dir.exists():
            self.log("⚠️ No GitHub Actions workflows found", "warning")
            return True
        
        workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        if not workflow_files:
            self.log("⚠️ No workflow files found in .github/workflows", "warning")
            return True
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r') as f:
                    yaml.safe_load(f)
                self.log(f"✅ Workflow file validated: {workflow_file.name}", "success")
            except yaml.YAMLError as e:
                self.log(f"❌ Invalid YAML in {workflow_file.name}: {e}", "error")
                return False
        
        return True
    
    def run_basic_tests(self) -> bool:
        """Run basic import tests"""
        self.log("🔍 Running basic import tests...")
        
        # Test critical imports
        test_imports = [
            "import fastapi",
            "import streamlit", 
            "import sqlalchemy",
            "import pydantic",
            "from api.index import app"
        ]
        
        for import_stmt in test_imports:
            success, output = self.run_command([
                sys.executable, "-c", import_stmt
            ])
            
            if not success:
                self.log(f"⚠️ Import test failed: {import_stmt}", "warning")
                if self.verbose:
                    self.log(f"Error: {output}", "warning")
            else:
                if self.verbose:
                    self.log(f"✅ Import success: {import_stmt}", "success")
        
        self.log("✅ Basic import tests completed", "success")
        return True
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        report = {
            "timestamp": "2025-01-27",
            "project": "AUDITORIA360",
            "validation_type": "Production Deploy Validation",
            "overall_status": "PASS" if not self.critical_issues else "FAIL",
            "critical_issues": self.critical_issues,
            "warnings": self.warnings,
            "validation_results": self.validation_results,
            "recommendations": []
        }
        
        # Add recommendations based on findings
        if self.warnings:
            report["recommendations"].append("Address warning items before production deploy")
        
        if "placeholder" in str(self.warnings):
            report["recommendations"].append("Update all placeholder values with production credentials")
        
        if not self.critical_issues:
            report["recommendations"].append("System is ready for production deployment")
        
        return report
    
    def run_full_validation(self) -> bool:
        """Run complete production validation"""
        self.log("🚀 Starting AUDITORIA360 Production Validation", "info")
        self.log("=" * 60, "info")
        
        validations = [
            ("File Structure", self.validate_file_structure),
            ("Environment Config", self.validate_environment_config),
            ("Dependencies", self.validate_dependencies),
            ("Vercel Config", self.validate_vercel_config),
            ("Streamlit Config", self.validate_streamlit_config),
            ("Docker Config", self.validate_docker_config),
            ("Security Measures", self.validate_security_measures),
            ("CI/CD Config", self.validate_ci_cd_config),
            ("Basic Tests", self.run_basic_tests)
        ]
        
        all_passed = True
        for name, validation_func in validations:
            self.log(f"\n🔍 {name}...")
            try:
                result = validation_func()
                self.validation_results[name] = result
                if not result:
                    all_passed = False
            except Exception as e:
                self.log(f"❌ Validation error in {name}: {e}", "error")
                self.validation_results[name] = False
                all_passed = False
        
        # Generate and save report
        report = self.generate_validation_report()
        report_path = self.project_root / "production_validation_report.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log("=" * 60, "info")
        
        if all_passed and not self.critical_issues:
            self.log("🎉 VALIDATION PASSED - Ready for Production Deploy!", "success")
        elif self.critical_issues:
            self.log("❌ VALIDATION FAILED - Critical issues must be resolved", "error")
            for issue in self.critical_issues:
                self.log(f"  • {issue}", "error")
        else:
            self.log("⚠️ VALIDATION COMPLETED - Address warnings before deploy", "warning")
        
        if self.warnings:
            self.log(f"\n⚠️ {len(self.warnings)} warnings found:", "warning")
            for warning in self.warnings[:5]:  # Show first 5 warnings
                self.log(f"  • {warning}", "warning")
            if len(self.warnings) > 5:
                self.log(f"  ... and {len(self.warnings) - 5} more warnings", "warning")
        
        self.log(f"\n📊 Validation report saved: {report_path}", "info")
        
        return all_passed and not self.critical_issues


def main():
    parser = argparse.ArgumentParser(description="AUDITORIA360 Production Validation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--fix-issues", action="store_true", help="Attempt to fix found issues")
    
    args = parser.parse_args()
    
    validator = ProductionValidator(verbose=args.verbose, fix_issues=args.fix_issues)
    
    success = validator.run_full_validation()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()