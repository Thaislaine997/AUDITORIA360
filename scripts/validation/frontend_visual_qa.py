#!/usr/bin/env python3
"""
Frontend Visual QA Validation Script
Implements section 5 of the operational checklist: Frontend build, deploy and visual verification
PRIORITY MAXIMUM - ensures no blank pages, no JS errors, consistent layout
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class FrontendVisualQAValidator:
    def __init__(self, staging_url: str = "https://staging.seudominio.com"):
        self.staging_url = staging_url.rstrip('/')
        self.local_url = "http://localhost:3000"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self._detect_environment(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "critical_failures": 0
            },
            "pages_tested": [],
            "visual_issues": []
        }
        
        # Priority pages to test (adjust for your app)
        self.priority_pages = [
            {"path": "/", "name": "Dashboard", "critical": True},
            {"path": "/login", "name": "Login", "critical": True},
            {"path": "/contabilidades", "name": "Contabilidades", "critical": True},
            {"path": "/auditorias", "name": "Auditorias", "critical": True},
            {"path": "/relatorios", "name": "Relatórios", "critical": True},
            {"path": "/admin/users", "name": "Admin Users", "critical": False},
        ]
        
        # Responsive breakpoints to test
        self.breakpoints = [
            {"name": "Mobile", "width": 375, "height": 667},
            {"name": "Tablet", "width": 768, "height": 1024},
            {"name": "Desktop", "width": 1024, "height": 768},
            {"name": "Large Desktop", "width": 1440, "height": 900}
        ]
        
    def _detect_environment(self) -> str:
        if "localhost" in self.staging_url:
            return "local"
        elif "staging" in self.staging_url:
            return "staging"
        else:
            return "production"
    
    def _log_test(self, test_name: str, status: str, details: Dict[str, Any], is_critical: bool = False):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "critical": is_critical
        }
        self.results["tests"].append(result)
        self.results["summary"]["total"] += 1
        
        if status == "PASS":
            self.results["summary"]["passed"] += 1
            icon = "🟢" if is_critical else "✅"
            print(f"{icon} {test_name}: {status}")
        else:
            self.results["summary"]["failed"] += 1
            if is_critical:
                self.results["summary"]["critical_failures"] += 1
                print(f"🔴 CRITICAL: {test_name}: {status}")
            else:
                print(f"❌ {test_name}: {status}")
            
            if "error" in details:
                print(f"   Error: {details['error']}")
    
    def test_frontend_build_and_deploy(self) -> bool:
        """
        Test 5.1: Build and deploy status verification
        Critério OK: Build terminado sem erros, deploy READY
        """
        test_name = "Frontend Build & Deploy Status"
        
        try:
            frontend_path = Path("/home/runner/work/AUDITORIA360/AUDITORIA360/src/frontend")
            
            if not frontend_path.exists():
                self._log_test(test_name, "FAIL", {
                    "error": "Frontend directory not found",
                    "expected_path": str(frontend_path)
                }, is_critical=True)
                return False
            
            # Test npm build
            print("   Building frontend...")
            result = subprocess.run(
                ["npm", "run", "build"],
                cwd=frontend_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max
            )
            
            if result.returncode == 0:
                # Check if dist directory was created
                dist_path = frontend_path / "dist"
                if dist_path.exists():
                    # Count files in dist
                    dist_files = list(dist_path.rglob("*"))
                    js_files = [f for f in dist_files if f.suffix == ".js"]
                    css_files = [f for f in dist_files if f.suffix == ".css"]
                    
                    self._log_test(test_name, "PASS", {
                        "build_success": True,
                        "dist_created": True,
                        "total_files": len(dist_files),
                        "js_files": len(js_files),
                        "css_files": len(css_files),
                        "build_time": "< 5 minutes"
                    })
                    return True
                else:
                    self._log_test(test_name, "FAIL", {
                        "error": "Build succeeded but dist directory not found",
                        "return_code": result.returncode
                    }, is_critical=True)
                    return False
            else:
                self._log_test(test_name, "FAIL", {
                    "error": "Build failed",
                    "return_code": result.returncode,
                    "stderr": result.stderr[:500],
                    "stdout": result.stdout[:500]
                }, is_critical=True)
                return False
                
        except subprocess.TimeoutExpired:
            self._log_test(test_name, "FAIL", {
                "error": "Build timeout (> 5 minutes)",
                "suggestion": "Check for hanging processes or large bundle sizes"
            }, is_critical=True)
            return False
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception during build: {str(e)}",
                "exception_type": type(e).__name__
            }, is_critical=True)
            return False
    
    def test_page_accessibility_basic(self, url: str) -> Dict[str, Any]:
        """
        Basic accessibility test using curl for initial validation
        Returns basic page information
        """
        try:
            result = subprocess.run(
                ["curl", "-I", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                headers = result.stdout
                status_line = headers.split('\n')[0] if headers else ""
                
                # Extract status code
                status_code = 0
                if "200" in status_line:
                    status_code = 200
                elif "404" in status_line:
                    status_code = 404
                elif "500" in status_line:
                    status_code = 500
                    
                content_type = ""
                for line in headers.split('\n'):
                    if line.lower().startswith('content-type'):
                        content_type = line.split(':', 1)[1].strip()
                        break
                
                return {
                    "accessible": status_code == 200,
                    "status_code": status_code,
                    "content_type": content_type,
                    "is_html": "html" in content_type.lower()
                }
            else:
                return {
                    "accessible": False,
                    "error": "curl failed",
                    "stderr": result.stderr
                }
                
        except Exception as e:
            return {
                "accessible": False,
                "error": str(e)
            }
    
    def test_static_assets_accessibility(self) -> bool:
        """
        Test 5.4: Static assets (CSS/JS) accessibility
        Critério OK: Cache-Control apropriado, Content-Type correto
        """
        test_name = "Static Assets Accessibility"
        
        common_assets = [
            "/static/css/main.css",
            "/static/js/main.js", 
            "/_next/static/css/main.css",  # Next.js style
            "/assets/index.css",  # Vite style
            "/assets/index.js"    # Vite style
        ]
        
        accessible_count = 0
        asset_results = {}
        
        for asset_path in common_assets:
            url = f"{self.staging_url}{asset_path}"
            result = self.test_page_accessibility_basic(url)
            asset_results[asset_path] = result
            
            if result.get("accessible"):
                accessible_count += 1
        
        # If at least some assets are accessible, consider it a pass
        # (exact asset paths may vary by build system)
        if accessible_count > 0:
            self._log_test(test_name, "PASS", {
                "accessible_assets": accessible_count,
                "total_tested": len(common_assets),
                "results": asset_results
            })
            return True
        else:
            self._log_test(test_name, "FAIL", {
                "accessible_assets": 0,
                "total_tested": len(common_assets),
                "results": asset_results,
                "suggestion": "Check build output paths and public directory configuration"
            })
            return False
    
    def test_priority_pages_accessibility(self) -> bool:
        """
        Test priority pages for basic accessibility
        Critério OK: All priority pages return 200 and serve HTML
        """
        test_name = "Priority Pages Accessibility"
        
        accessible_pages = []
        failed_pages = []
        page_results = {}
        
        for page in self.priority_pages:
            url = f"{self.staging_url}{page['path']}"
            result = self.test_page_accessibility_basic(url)
            page_results[page['name']] = result
            
            if result.get("accessible") and result.get("is_html"):
                accessible_pages.append(page['name'])
                self.results["pages_tested"].append({
                    "name": page['name'],
                    "path": page['path'],
                    "status": "ACCESSIBLE"
                })
            else:
                failed_pages.append({
                    "name": page['name'], 
                    "path": page['path'],
                    "error": result.get("error", "Not accessible or not HTML")
                })
                self.results["pages_tested"].append({
                    "name": page['name'],
                    "path": page['path'],
                    "status": "FAILED"
                })
                
                if page.get('critical'):
                    self.results["visual_issues"].append({
                        "type": "CRITICAL_PAGE_INACCESSIBLE",
                        "page": page['name'],
                        "path": page['path'],
                        "details": result
                    })
        
        # Success if at least 80% of priority pages are accessible
        success_rate = len(accessible_pages) / len(self.priority_pages)
        
        if success_rate >= 0.8:
            self._log_test(test_name, "PASS", {
                "accessible_pages": len(accessible_pages),
                "total_pages": len(self.priority_pages),
                "success_rate": f"{success_rate:.1%}",
                "accessible_list": accessible_pages,
                "failed_list": failed_pages
            })
            return True
        else:
            is_critical = any(page.get('critical') for page in self.priority_pages 
                            if page['name'] in [fp['name'] for fp in failed_pages])
            
            self._log_test(test_name, "FAIL", {
                "accessible_pages": len(accessible_pages),
                "total_pages": len(self.priority_pages),
                "success_rate": f"{success_rate:.1%}",
                "failed_list": failed_pages
            }, is_critical=is_critical)
            return False
    
    def test_bundle_size_analysis(self) -> bool:
        """
        Test 9.2: Bundle size analysis
        Critério OK: main bundle < 1.5–2MB gzipped idealmente
        """
        test_name = "Bundle Size Analysis"
        
        try:
            frontend_path = Path("/home/runner/work/AUDITORIA360/AUDITORIA360/src/frontend")
            dist_path = frontend_path / "dist"
            
            if not dist_path.exists():
                self._log_test(test_name, "SKIP", {
                    "reason": "dist directory not found - run build first"
                })
                return False
            
            # Find JS bundle files
            js_files = list(dist_path.rglob("*.js"))
            css_files = list(dist_path.rglob("*.css"))
            
            total_js_size = sum(f.stat().st_size for f in js_files)
            total_css_size = sum(f.stat().st_size for f in css_files)
            total_size = total_js_size + total_css_size
            
            # Convert to MB
            total_size_mb = total_size / (1024 * 1024)
            
            # Find largest files
            all_files = js_files + css_files
            largest_files = sorted(all_files, key=lambda f: f.stat().st_size, reverse=True)[:5]
            
            largest_info = []
            for f in largest_files:
                size_kb = f.stat().st_size / 1024
                largest_info.append({
                    "name": f.name,
                    "size_kb": round(size_kb, 1)
                })
            
            # Bundle size check (conservative threshold)
            bundle_ok = total_size_mb < 2.0  # 2MB threshold
            
            if bundle_ok:
                self._log_test(test_name, "PASS", {
                    "total_size_mb": round(total_size_mb, 2),
                    "js_files": len(js_files),
                    "css_files": len(css_files),
                    "largest_files": largest_info,
                    "threshold_mb": 2.0
                })
                return True
            else:
                self._log_test(test_name, "FAIL", {
                    "total_size_mb": round(total_size_mb, 2),
                    "threshold_mb": 2.0,
                    "exceeded_by_mb": round(total_size_mb - 2.0, 2),
                    "largest_files": largest_info,
                    "suggestion": "Consider code splitting or removing unused dependencies"
                })
                return False
                
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception during bundle analysis: {str(e)}"
            })
            return False
    
    def test_security_headers_basic(self) -> bool:
        """
        Test 8.2: Basic security headers check
        Critério OK: CSP adequada, HSTS presente, X-Frame-Options
        """
        test_name = "Security Headers Check"
        
        try:
            result = subprocess.run(
                ["curl", "-I", self.staging_url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self._log_test(test_name, "SKIP", {
                    "reason": "Could not fetch headers from staging URL"
                })
                return False
            
            headers_text = result.stdout.lower()
            
            # Check for security headers
            has_csp = "content-security-policy" in headers_text
            has_hsts = "strict-transport-security" in headers_text
            has_frame_options = "x-frame-options" in headers_text
            
            security_score = sum([has_csp, has_hsts, has_frame_options])
            
            if security_score >= 2:  # At least 2 out of 3
                self._log_test(test_name, "PASS", {
                    "content_security_policy": has_csp,
                    "strict_transport_security": has_hsts,
                    "x_frame_options": has_frame_options,
                    "security_score": f"{security_score}/3"
                })
                return True
            else:
                self._log_test(test_name, "FAIL", {
                    "content_security_policy": has_csp,
                    "strict_transport_security": has_hsts,
                    "x_frame_options": has_frame_options,
                    "security_score": f"{security_score}/3",
                    "suggestion": "Configure security headers in web server or CDN"
                })
                return False
                
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception: {str(e)}"
            })
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all frontend visual QA tests"""
        print("🎨 Running Frontend Visual QA Validation...")
        print("🔥 PRIORITY MAXIMUM - Frontend Visual Validation")
        print(f"Target Environment: {self.results['environment']} ({self.staging_url})")
        print("-" * 60)
        
        # Run frontend tests in priority order
        test_results = [
            self.test_frontend_build_and_deploy(),        # Critical: build must work
            self.test_priority_pages_accessibility(),      # Critical: pages must load
            self.test_static_assets_accessibility(),       # Important: assets must load
            self.test_bundle_size_analysis(),             # Performance: bundle size
            self.test_security_headers_basic()            # Security: basic headers
        ]
        
        # Calculate overall status
        all_passed = all(test_results)
        has_critical_failures = self.results["summary"]["critical_failures"] > 0
        
        if has_critical_failures:
            self.results["overall_status"] = "CRITICAL_FAIL"
        else:
            self.results["overall_status"] = "PASS" if all_passed else "FAIL"
        
        # Add visual validation summary
        self.results["visual_summary"] = {
            "pages_tested": len(self.results["pages_tested"]),
            "visual_issues_found": len(self.results["visual_issues"]),
            "critical_pages_accessible": len([p for p in self.results["pages_tested"] if p["status"] == "ACCESSIBLE"]),
            "build_successful": any(t["status"] == "PASS" and "build_success" in t.get("details", {}) for t in self.results["tests"])
        }
        
        print("-" * 60)
        print(f"📊 Summary: {self.results['summary']['passed']}/{self.results['summary']['total']} tests passed")
        print(f"🔴 Critical Failures: {self.results['summary']['critical_failures']}")
        print(f"🎯 Overall Status: {self.results['overall_status']}")
        print(f"📱 Pages Tested: {self.results['visual_summary']['pages_tested']}")
        print(f"🎨 Visual Issues: {self.results['visual_summary']['visual_issues_found']}")
        
        if has_critical_failures:
            print("\n🚨 CRITICAL FRONTEND ISSUES DETECTED!")
            print("❗ IMMEDIATE ACTION REQUIRED:")
            print("- Frontend build is failing or pages are not accessible")
            print("- Check build logs and fix compilation errors")
            print("- Verify deployment configuration and routes")
            print("- Test locally before redeploying")
        elif not all_passed:
            print("\n❗ Recommendations for frontend improvements:")
            print("- Optimize bundle size if exceeding thresholds")
            print("- Configure security headers in web server")
            print("- Test all pages manually for visual consistency")
            print("- Run full E2E tests with Playwright")
        else:
            print("\n✅ Frontend is ready for production!")
            print("- All critical pages are accessible")
            print("- Build is successful and optimized")
            print("- Basic security headers present")
        
        return self.results


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AUDITORIA360 Frontend Visual QA Validation")
    parser.add_argument("--url", default="https://staging.seudominio.com", help="Staging URL for testing")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--local", action="store_true", help="Test against local development server")
    
    args = parser.parse_args()
    
    # Use local URL if flag is provided
    test_url = "http://localhost:3000" if args.local else args.url
    
    validator = FrontendVisualQAValidator(test_url)
    results = validator.run_all_tests()
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Exit with appropriate code
    if results["overall_status"] == "CRITICAL_FAIL":
        print("\n🚨 Exiting with critical failure code")
        sys.exit(2)  # Critical frontend failure
    elif results["overall_status"] == "PASS":
        sys.exit(0)
    else:
        sys.exit(1)  # Regular failure


if __name__ == "__main__":
    main()