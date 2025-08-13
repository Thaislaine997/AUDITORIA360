#!/usr/bin/env python3
"""
Backend Health Check Validation Script
Implements section 2 of the operational checklist: Backend / Health checks (FastAPI)
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any, List
from urllib.parse import urlparse

# Configuration
BASE_URL = os.getenv("TEST_API_URL", "http://localhost:8000")
STAGING_URL = os.getenv("STAGING_API_URL", "https://staging.seudominio.com")


class HealthCheckValidator:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self._detect_environment(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0
            }
        }
        
    def _detect_environment(self) -> str:
        """Detect if running against local, staging, or production"""
        if "localhost" in self.base_url or "127.0.0.1" in self.base_url:
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
        else:
            self.results["summary"]["failed"] += 1
            print(f"❌ {test_name}: {status}")
            if "error" in details:
                print(f"   Error: {details['error']}")
    
    def test_health_endpoint(self) -> bool:
        """
        Test 2.1: Health endpoint
        Critério OK: status 200 e payload com status: ok (ou similar)
        """
        test_name = "Health Endpoint Check"
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") in ["ok", "healthy"]:
                    self._log_test(test_name, "PASS", {
                        "status_code": response.status_code,
                        "response_time": response.elapsed.total_seconds(),
                        "payload": data
                    })
                    return True
                else:
                    self._log_test(test_name, "FAIL", {
                        "status_code": response.status_code,
                        "error": f"Invalid status: {data.get('status')}",
                        "payload": data
                    })
            else:
                self._log_test(test_name, "FAIL", {
                    "status_code": response.status_code,
                    "error": f"Expected 200, got {response.status_code}"
                })
                
        except requests.exceptions.RequestException as e:
            self._log_test(test_name, "FAIL", {
                "error": str(e),
                "suggestion": "Check if API is running and accessible"
            })
            
        return False
    
    def test_smoke_auth_login(self) -> bool:
        """
        Test 2.2: Smoke test for auth endpoints
        Critério OK: retorna token JWT e 200
        """
        test_name = "Auth Login Smoke Test"
        try:
            login_data = {
                "email": "contab_a@demo.local",
                "password": "demo123"
            }
            
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self._log_test(test_name, "PASS", {
                        "status_code": response.status_code,
                        "has_token": True,
                        "response_time": response.elapsed.total_seconds()
                    })
                    return True
                else:
                    self._log_test(test_name, "FAIL", {
                        "status_code": response.status_code,
                        "error": "No access_token in response",
                        "payload": data
                    })
            else:
                self._log_test(test_name, "FAIL", {
                    "status_code": response.status_code,
                    "error": f"Expected 200, got {response.status_code}",
                    "response_text": response.text[:200]
                })
                
        except requests.exceptions.RequestException as e:
            self._log_test(test_name, "FAIL", {
                "error": str(e),
                "suggestion": "Check auth endpoint configuration and demo users"
            })
            
        return False
    
    def test_api_contract_openapi(self) -> bool:
        """
        Test 2.3: API contract / OpenAPI
        Critério OK: OpenAPI renderiza; testes de rota simples via UI funcionam
        """
        test_name = "OpenAPI Documentation Check"
        try:
            # Test /docs endpoint
            docs_response = requests.get(f"{self.base_url}/docs", timeout=10)
            openapi_response = requests.get(f"{self.base_url}/openapi.json", timeout=10)
            
            docs_ok = docs_response.status_code == 200 and "html" in docs_response.headers.get("content-type", "")
            openapi_ok = openapi_response.status_code == 200
            
            if docs_ok and openapi_ok:
                openapi_data = openapi_response.json()
                self._log_test(test_name, "PASS", {
                    "docs_status": docs_response.status_code,
                    "openapi_status": openapi_response.status_code,
                    "api_title": openapi_data.get("info", {}).get("title", ""),
                    "api_version": openapi_data.get("info", {}).get("version", ""),
                    "endpoint_count": len(openapi_data.get("paths", {}))
                })
                return True
            else:
                self._log_test(test_name, "FAIL", {
                    "docs_status": docs_response.status_code,
                    "openapi_status": openapi_response.status_code,
                    "error": "OpenAPI docs not accessible"
                })
                
        except requests.exceptions.RequestException as e:
            self._log_test(test_name, "FAIL", {
                "error": str(e),
                "suggestion": "Check if FastAPI app is configured with docs enabled"
            })
            
        return False
    
    def test_critical_endpoints(self) -> bool:
        """
        Test additional critical endpoints for smoke testing
        """
        test_name = "Critical Endpoints Smoke Test"
        critical_endpoints = [
            "/",  # Root health
            "/health",  # Detailed health
            "/api/v1/auditorias/options/contabilidades",  # Legacy endpoint
        ]
        
        passed_count = 0
        endpoint_results = {}
        
        for endpoint in critical_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                is_ok = response.status_code in [200, 201]
                endpoint_results[endpoint] = {
                    "status_code": response.status_code,
                    "ok": is_ok,
                    "response_time": response.elapsed.total_seconds()
                }
                if is_ok:
                    passed_count += 1
                    
            except requests.exceptions.RequestException as e:
                endpoint_results[endpoint] = {
                    "error": str(e),
                    "ok": False
                }
        
        success_rate = passed_count / len(critical_endpoints)
        if success_rate >= 0.8:  # 80% success rate
            self._log_test(test_name, "PASS", {
                "success_rate": f"{success_rate:.1%}",
                "passed": passed_count,
                "total": len(critical_endpoints),
                "results": endpoint_results
            })
            return True
        else:
            self._log_test(test_name, "FAIL", {
                "success_rate": f"{success_rate:.1%}",
                "passed": passed_count,
                "total": len(critical_endpoints),
                "results": endpoint_results
            })
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all health check tests"""
        print("🏥 Running Backend Health Check Validation...")
        print(f"Target Environment: {self.results['environment']} ({self.base_url})")
        print("-" * 60)
        
        # Run all health tests
        test_results = [
            self.test_health_endpoint(),
            self.test_smoke_auth_login(),
            self.test_api_contract_openapi(),
            self.test_critical_endpoints()
        ]
        
        # Calculate overall status
        all_passed = all(test_results)
        self.results["overall_status"] = "PASS" if all_passed else "FAIL"
        
        print("-" * 60)
        print(f"📊 Summary: {self.results['summary']['passed']}/{self.results['summary']['total']} tests passed")
        print(f"🎯 Overall Status: {self.results['overall_status']}")
        
        if not all_passed:
            print("\n❗ Remediation suggestions:")
            print("- Check if API server is running and accessible")
            print("- Verify demo users are created (contab_a@demo.local)")
            print("- Check environment variables and database connection")
            print("- Review logs for detailed error information")
        
        return self.results


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AUDITORIA360 Health Check Validation")
    parser.add_argument("--url", default=BASE_URL, help="Base URL for API testing")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--staging", action="store_true", help="Test against staging environment")
    
    args = parser.parse_args()
    
    # Use staging URL if flag is provided
    test_url = STAGING_URL if args.staging else args.url
    
    validator = HealthCheckValidator(test_url)
    results = validator.run_all_tests()
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Exit with error code if tests failed
    sys.exit(0 if results["overall_status"] == "PASS" else 1)


if __name__ == "__main__":
    main()