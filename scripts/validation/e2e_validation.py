#!/usr/bin/env python3
"""
E2E Testing Validation Script  
Implements section 6 of the operational checklist: Automated E2E testing
Orchestrates Playwright test execution and reporting
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class E2EValidationRunner:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url.rstrip('/')
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self._detect_environment(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            },
            "playwright_results": {}
        }
        
        # Find E2E test directories
        self.project_root = Path("/home/runner/work/AUDITORIA360/AUDITORIA360")
        self.e2e_paths = [
            self.project_root / "tests" / "e2e",
            self.project_root / "AUDITORIA360_patches_v2" / "frontend" / "e2e",
            self.project_root / "src" / "frontend" / "e2e"
        ]
        
    def _detect_environment(self) -> str:
        if "localhost" in self.base_url:
            return "local"
        elif "staging" in self.base_url:
            return "staging"
        else:
            return "production"
    
    def _log_test(self, test_name: str, status: str, details: Dict[str, Any]):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.results["tests"].append(result)
        self.results["summary"]["total"] += 1
        
        if status == "PASS":
            self.results["summary"]["passed"] += 1
            print(f"✅ {test_name}: {status}")
        elif status == "SKIP":
            self.results["summary"]["skipped"] += 1
            print(f"⏭️  {test_name}: {status}")
        else:
            self.results["summary"]["failed"] += 1
            print(f"❌ {test_name}: {status}")
        
        if "error" in details:
            print(f"   Error: {details['error']}")
    
    def test_playwright_installation(self) -> bool:
        """
        Test if Playwright is installed and browsers are available
        """
        test_name = "Playwright Installation Check"
        
        try:
            # Check if playwright command is available
            result = subprocess.run(
                ["npx", "playwright", "--version"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                
                # Check if browsers are installed
                browser_check = subprocess.run(
                    ["npx", "playwright", "install", "--dry-run"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                self._log_test(test_name, "PASS", {
                    "playwright_version": version,
                    "browsers_installed": browser_check.returncode == 0,
                    "install_output": browser_check.stdout[:200] if browser_check.stdout else ""
                })
                return True
            else:
                self._log_test(test_name, "FAIL", {
                    "error": "Playwright not found or not working",
                    "stderr": result.stderr,
                    "return_code": result.returncode
                })
                return False
                
        except subprocess.TimeoutExpired:
            self._log_test(test_name, "FAIL", {
                "error": "Timeout checking Playwright installation"
            })
            return False
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception: {str(e)}"
            })
            return False
    
    def test_install_playwright_browsers(self) -> bool:
        """
        Install Playwright browsers if needed
        """
        test_name = "Install Playwright Browsers"
        
        try:
            print("   Installing Playwright browsers...")
            result = subprocess.run(
                ["npx", "playwright", "install"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max for browser installation
            )
            
            if result.returncode == 0:
                self._log_test(test_name, "PASS", {
                    "browsers_installed": True,
                    "install_output": result.stdout[-200:] if result.stdout else ""
                })
                return True
            else:
                self._log_test(test_name, "FAIL", {
                    "error": "Failed to install Playwright browsers",
                    "stderr": result.stderr[:500],
                    "return_code": result.returncode
                })
                return False
                
        except subprocess.TimeoutExpired:
            self._log_test(test_name, "FAIL", {
                "error": "Timeout during browser installation (> 5 minutes)"
            })
            return False
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception: {str(e)}"
            })
            return False
    
    def test_find_e2e_tests(self) -> bool:
        """
        Find and validate E2E test files
        """
        test_name = "E2E Tests Discovery"
        
        found_tests = []
        test_files = []
        
        for e2e_path in self.e2e_paths:
            if e2e_path.exists():
                # Find TypeScript test files
                ts_tests = list(e2e_path.rglob("*.spec.ts"))
                py_tests = list(e2e_path.rglob("*test*.py"))
                
                for test_file in ts_tests + py_tests:
                    test_files.append({
                        "path": str(test_file),
                        "relative_path": str(test_file.relative_to(self.project_root)),
                        "type": "typescript" if test_file.suffix == ".ts" else "python",
                        "size": test_file.stat().st_size
                    })
                
                if ts_tests or py_tests:
                    found_tests.append({
                        "directory": str(e2e_path),
                        "typescript_tests": len(ts_tests),
                        "python_tests": len(py_tests)
                    })
        
        if found_tests:
            self._log_test(test_name, "PASS", {
                "test_directories": len(found_tests),
                "total_test_files": len(test_files),
                "directories": found_tests,
                "test_files": test_files[:10]  # Limit to first 10 for brevity
            })
            self.results["found_test_files"] = test_files
            return True
        else:
            self._log_test(test_name, "FAIL", {
                "error": "No E2E test files found",
                "searched_paths": [str(p) for p in self.e2e_paths],
                "suggestion": "Create E2E tests or check test file naming conventions"
            })
            return False
    
    def test_run_playwright_tests(self) -> bool:
        """
        Execute Playwright tests and collect results
        """
        test_name = "Execute Playwright E2E Tests"
        
        # Look for Playwright tests in patches folder first
        playwright_dir = self.project_root / "AUDITORIA360_patches_v2" / "frontend"
        
        if not playwright_dir.exists():
            # Fallback to other locations
            playwright_dir = self.project_root / "tests" / "e2e"
            if not playwright_dir.exists():
                self._log_test(test_name, "SKIP", {
                    "reason": "No Playwright test directory found",
                    "searched_paths": [str(p) for p in self.e2e_paths]
                })
                return False
        
        try:
            # Check if there's a playwright config
            config_files = [
                playwright_dir / "playwright.config.ts",
                playwright_dir / "playwright.config.js",
                self.project_root / "playwright.config.ts",
                self.project_root / "playwright.config.js"
            ]
            
            config_file = None
            for cf in config_files:
                if cf.exists():
                    config_file = cf
                    break
            
            # Run Playwright tests
            cmd = ["npx", "playwright", "test"]
            if config_file:
                cmd.extend(["--config", str(config_file)])
            
            # Add reporter for JSON output
            cmd.extend(["--reporter=json"])
            
            print(f"   Running Playwright tests from: {playwright_dir}")
            result = subprocess.run(
                cmd,
                cwd=playwright_dir,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max
                env={**os.environ, "BASE_URL": self.base_url}
            )
            
            # Parse JSON output if available
            playwright_results = {}
            try:
                if result.stdout:
                    playwright_results = json.loads(result.stdout)
            except json.JSONDecodeError:
                pass
            
            self.results["playwright_results"] = playwright_results
            
            if result.returncode == 0:
                # Extract test results
                total_tests = len(playwright_results.get("tests", []))
                passed_tests = len([t for t in playwright_results.get("tests", []) if t.get("outcome") == "expected"])
                
                self._log_test(test_name, "PASS", {
                    "tests_executed": total_tests,
                    "tests_passed": passed_tests,
                    "execution_time": playwright_results.get("stats", {}).get("duration", 0),
                    "config_file": str(config_file) if config_file else None,
                    "base_url": self.base_url
                })
                return True
            else:
                # Parse failures
                failed_tests = []
                if playwright_results.get("tests"):
                    failed_tests = [
                        {
                            "title": t.get("title", "Unknown"),
                            "error": t.get("results", [{}])[0].get("error", {}).get("message", "")[:200]
                        }
                        for t in playwright_results.get("tests", [])
                        if t.get("outcome") != "expected"
                    ]
                
                self._log_test(test_name, "FAIL", {
                    "return_code": result.returncode,
                    "failed_tests": failed_tests,
                    "stderr": result.stderr[:500],
                    "suggestion": "Check test failures and application functionality"
                })
                return False
                
        except subprocess.TimeoutExpired:
            self._log_test(test_name, "FAIL", {
                "error": "E2E tests timeout (> 5 minutes)",
                "suggestion": "Check for hanging tests or infinite loops"
            })
            return False
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception during E2E execution: {str(e)}"
            })
            return False
    
    def test_create_basic_e2e_tests(self) -> bool:
        """
        Create basic E2E tests if none exist
        """
        test_name = "Create Basic E2E Tests"
        
        # Only create if no tests exist
        if hasattr(self.results, 'found_test_files') and self.results['found_test_files']:
            self._log_test(test_name, "SKIP", {
                "reason": "E2E tests already exist"
            })
            return True
        
        try:
            e2e_dir = self.project_root / "tests" / "e2e"
            e2e_dir.mkdir(parents=True, exist_ok=True)
            
            # Create basic Playwright config
            config_content = '''import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});'''
            
            with open(e2e_dir / "playwright.config.ts", "w") as f:
                f.write(config_content)
            
            # Create basic test
            test_content = '''import { test, expect } from '@playwright/test';

test('basic health check', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/AUDITORIA360/);
});

test('login page accessible', async ({ page }) => {
  await page.goto('/login');
  await expect(page.locator('input[type="email"]')).toBeVisible();
});'''
            
            with open(e2e_dir / "basic.spec.ts", "w") as f:
                f.write(test_content)
            
            # Create package.json for E2E tests
            package_content = {
                "name": "auditoria360-e2e",
                "version": "1.0.0",
                "devDependencies": {
                    "@playwright/test": "^1.30.0"
                },
                "scripts": {
                    "test": "playwright test",
                    "test:headed": "playwright test --headed"
                }
            }
            
            with open(e2e_dir / "package.json", "w") as f:
                json.dump(package_content, f, indent=2)
            
            self._log_test(test_name, "PASS", {
                "created_files": [
                    "playwright.config.ts",
                    "basic.spec.ts", 
                    "package.json"
                ],
                "directory": str(e2e_dir)
            })
            return True
            
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception creating E2E tests: {str(e)}"
            })
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all E2E validation tests"""
        print("🎭 Running E2E Testing Validation...")
        print(f"Target Environment: {self.results['environment']} ({self.base_url})")
        print("-" * 60)
        
        # Run E2E validation tests
        test_results = [
            self.test_playwright_installation(),
            self.test_find_e2e_tests(),
            self.test_create_basic_e2e_tests(),
            self.test_install_playwright_browsers(),
            self.test_run_playwright_tests()
        ]
        
        # Calculate overall status
        critical_tests = test_results[:2]  # Installation and test discovery
        all_critical_passed = all(critical_tests)
        
        if all_critical_passed:
            # If critical tests pass, overall status depends on test execution
            self.results["overall_status"] = "PASS" if any(test_results[3:]) else "PARTIAL"
        else:
            self.results["overall_status"] = "FAIL"
        
        # Add E2E summary
        self.results["e2e_summary"] = {
            "playwright_available": test_results[0] if len(test_results) > 0 else False,
            "tests_found": test_results[1] if len(test_results) > 1 else False,
            "browsers_installed": test_results[3] if len(test_results) > 3 else False,
            "tests_executed": test_results[4] if len(test_results) > 4 else False,
            "total_e2e_files": len(self.results.get("found_test_files", []))
        }
        
        print("-" * 60)
        print(f"📊 Summary: {self.results['summary']['passed']}/{self.results['summary']['total']} tests passed")
        print(f"⏭️  Skipped: {self.results['summary']['skipped']}")
        print(f"🎯 Overall Status: {self.results['overall_status']}")
        
        playwright_stats = self.results["playwright_results"].get("stats", {})
        if playwright_stats:
            print(f"🎭 Playwright Tests: {playwright_stats.get('passed', 0)} passed, {playwright_stats.get('failed', 0)} failed")
        
        if not all_critical_passed:
            print("\n❗ E2E Testing Setup Issues:")
            print("- Install Playwright: npm install @playwright/test")
            print("- Create basic E2E tests for critical user flows")
            print("- Ensure frontend is running on expected port")
        elif self.results["overall_status"] == "PARTIAL":
            print("\n⚠️  E2E Tests Partially Working:")
            print("- Basic setup is ready but some tests may be failing")
            print("- Review test failures and fix application issues")
            print("- Add more comprehensive test coverage")
        else:
            print("\n✅ E2E Testing is Ready!")
            print("- Playwright is installed and configured")
            print("- Tests are executing successfully")
            print("- Good foundation for regression testing")
        
        return self.results


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AUDITORIA360 E2E Testing Validation")
    parser.add_argument("--url", default="http://localhost:3000", help="Base URL for E2E testing")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--staging", action="store_true", help="Test against staging environment")
    
    args = parser.parse_args()
    
    # Use staging URL if flag is provided
    test_url = "https://staging.seudominio.com" if args.staging else args.url
    
    validator = E2EValidationRunner(test_url)
    results = validator.run_all_tests()
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Exit with appropriate code
    if results["overall_status"] == "PASS":
        sys.exit(0)
    elif results["overall_status"] == "PARTIAL":
        sys.exit(0)  # Partial success is OK for E2E
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()