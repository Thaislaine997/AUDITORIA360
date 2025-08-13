#!/usr/bin/env python3
"""
Row Level Security (RLS) Validation Script
Implements section 3 of the operational checklist: Database & RLS (multi-tenant) validation
Critical for LGPD compliance - ensures proper data isolation between tenants
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple


class RLSSecurityValidator:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self._detect_environment(),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "critical_failures": 0  # RLS failures are critical for LGPD
            }
        }
        
        # Demo tenant credentials - adjust for your environment
        self.tenant_a_creds = {
            "email": "contab_a@demo.local",
            "password": "demo123"
        }
        self.tenant_b_creds = {
            "email": "contab_b@demo.local", 
            "password": "demo123"
        }
        
    def _detect_environment(self) -> str:
        """Detect if running against local, staging, or production"""
        if "localhost" in self.base_url or "127.0.0.1" in self.base_url:
            return "local"
        elif "staging" in self.base_url:
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
    
    def _login(self, email: str, password: str) -> Optional[str]:
        """Login and return access token"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"email": email, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("access_token")
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
    
    def _create_cliente(self, token: str, payload: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Create a client record"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{self.base_url}/api/contabilidade/clientes",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
    
    def _get_cliente(self, token: str, cliente_id: str) -> Tuple[Optional[Dict[str, Any]], int]:
        """Get a client record and return data + status code"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{self.base_url}/api/contabilidade/clientes/{cliente_id}",
                headers=headers,
                timeout=10
            )
            
            data = None
            if response.status_code == 200:
                try:
                    data = response.json()
                except:
                    data = {"raw_response": response.text}
                    
            return data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return None, -1
    
    def test_rls_isolation_core(self) -> bool:
        """
        Core RLS isolation test - tenant B should NOT access tenant A's data
        This is CRITICAL for LGPD compliance
        """
        test_name = "RLS Core Isolation Test"
        
        try:
            # Step 1: Login both tenants
            token_a = self._login(self.tenant_a_creds["email"], self.tenant_a_creds["password"])
            token_b = self._login(self.tenant_b_creds["email"], self.tenant_b_creds["password"])
            
            if not token_a or not token_b:
                self._log_test(test_name, "FAIL", {
                    "error": "Could not authenticate demo tenants",
                    "token_a": bool(token_a),
                    "token_b": bool(token_b),
                    "suggestion": "Verify demo users exist and credentials are correct"
                }, is_critical=True)
                return False
            
            # Step 2: Tenant A creates a client
            payload = {
                "nome": f"Cliente Teste RLS {datetime.now().strftime('%H%M%S')}",
                "cnpj": "00000000000191",
                "email_contato": "teste@rls.isolation"
            }
            
            created_cliente = self._create_cliente(token_a, payload)
            if not created_cliente:
                self._log_test(test_name, "FAIL", {
                    "error": "Could not create client with tenant A",
                    "payload": payload
                }, is_critical=True)
                return False
            
            cliente_id = created_cliente.get("id")
            if not cliente_id:
                self._log_test(test_name, "FAIL", {
                    "error": "Created client has no ID",
                    "response": created_cliente
                }, is_critical=True)
                return False
            
            # Step 3: Tenant A can read their own data (control test)
            data_a, status_a = self._get_cliente(token_a, cliente_id)
            if status_a != 200:
                self._log_test(test_name, "FAIL", {
                    "error": "Tenant A cannot read their own data",
                    "status_code": status_a,
                    "cliente_id": cliente_id
                }, is_critical=True)
                return False
            
            # Step 4: Tenant B SHOULD NOT access tenant A's data
            data_b, status_b = self._get_cliente(token_b, cliente_id)
            
            # Critical check: Tenant B should get 403 or 404, NEVER 200 with data
            if status_b == 200 and data_b:
                # CRITICAL SECURITY VIOLATION - RLS is not working!
                self._log_test(test_name, "FAIL", {
                    "error": "CRITICAL: RLS VIOLATION - Tenant B accessed Tenant A's data",
                    "tenant_a_id": cliente_id,
                    "tenant_b_status": status_b,
                    "tenant_b_data": data_b,
                    "security_impact": "LGPD violation - data leak between tenants"
                }, is_critical=True)
                return False
            
            elif status_b in [403, 404]:
                # Good! RLS is working correctly
                self._log_test(test_name, "PASS", {
                    "tenant_a_created": True,
                    "tenant_a_can_read": status_a == 200,
                    "tenant_b_blocked": True,
                    "tenant_b_status": status_b,
                    "rls_working": True,
                    "lgpd_compliant": True
                }, is_critical=True)
                return True
            
            else:
                # Unexpected status - might indicate API issues
                self._log_test(test_name, "FAIL", {
                    "error": f"Unexpected status from tenant B: {status_b}",
                    "expected": "403 or 404",
                    "actual": status_b,
                    "suggestion": "Check API error handling and RLS policies"
                }, is_critical=True)
                return False
                
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception during RLS test: {str(e)}",
                "exception_type": type(e).__name__
            }, is_critical=True)
            return False
    
    def test_rls_bidirectional(self) -> bool:
        """
        Test RLS works in both directions (A can't see B, B can't see A)
        """
        test_name = "RLS Bidirectional Isolation Test"
        
        try:
            token_a = self._login(self.tenant_a_creds["email"], self.tenant_a_creds["password"])
            token_b = self._login(self.tenant_b_creds["email"], self.tenant_b_creds["password"])
            
            if not token_a or not token_b:
                self._log_test(test_name, "SKIP", {
                    "reason": "Could not authenticate tenants"
                })
                return False
            
            # Tenant B creates a client
            payload_b = {
                "nome": f"Cliente Tenant B {datetime.now().strftime('%H%M%S')}",
                "cnpj": "11111111111111",
                "email_contato": "tenant_b@test.com"
            }
            
            created_b = self._create_cliente(token_b, payload_b)
            if not created_b:
                self._log_test(test_name, "SKIP", {
                    "reason": "Could not create client with tenant B"
                })
                return False
            
            cliente_b_id = created_b.get("id")
            
            # Tenant A tries to read Tenant B's data
            data_a_tries_b, status_a_tries_b = self._get_cliente(token_a, cliente_b_id)
            
            if status_a_tries_b == 200 and data_a_tries_b:
                self._log_test(test_name, "FAIL", {
                    "error": "CRITICAL: Tenant A accessed Tenant B's data",
                    "status_code": status_a_tries_b
                }, is_critical=True)
                return False
            else:
                self._log_test(test_name, "PASS", {
                    "bidirectional_isolation": True,
                    "tenant_b_blocked_from_a": True,
                    "tenant_a_blocked_from_b": status_a_tries_b in [403, 404]
                }, is_critical=True)
                return True
                
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception: {str(e)}"
            }, is_critical=True)
            return False
    
    def test_tenant_list_isolation(self) -> bool:
        """
        Test that listing endpoints only return tenant-specific data
        """
        test_name = "RLS List Endpoints Isolation"
        
        try:
            token_a = self._login(self.tenant_a_creds["email"], self.tenant_a_creds["password"])
            token_b = self._login(self.tenant_b_creds["email"], self.tenant_b_creds["password"])
            
            if not token_a or not token_b:
                self._log_test(test_name, "SKIP", {"reason": "Could not authenticate"})
                return False
            
            # Get client lists for both tenants
            headers_a = {"Authorization": f"Bearer {token_a}"}
            headers_b = {"Authorization": f"Bearer {token_b}"}
            
            response_a = requests.get(f"{self.base_url}/api/contabilidade/clientes", headers=headers_a, timeout=10)
            response_b = requests.get(f"{self.base_url}/api/contabilidade/clientes", headers=headers_b, timeout=10)
            
            if response_a.status_code == 200 and response_b.status_code == 200:
                data_a = response_a.json()
                data_b = response_b.json()
                
                # Extract IDs from both lists
                ids_a = set()
                ids_b = set()
                
                if isinstance(data_a, list):
                    ids_a = {item.get("id") for item in data_a if item.get("id")}
                elif isinstance(data_a, dict) and "data" in data_a:
                    ids_a = {item.get("id") for item in data_a["data"] if item.get("id")}
                
                if isinstance(data_b, list):
                    ids_b = {item.get("id") for item in data_b if item.get("id")}
                elif isinstance(data_b, dict) and "data" in data_b:
                    ids_b = {item.get("id") for item in data_b["data"] if item.get("id")}
                
                # Check for overlap - there should be NONE
                overlap = ids_a.intersection(ids_b)
                
                if overlap:
                    self._log_test(test_name, "FAIL", {
                        "error": "CRITICAL: List endpoints show overlapping data between tenants",
                        "overlapping_ids": list(overlap),
                        "tenant_a_count": len(ids_a),
                        "tenant_b_count": len(ids_b)
                    }, is_critical=True)
                    return False
                else:
                    self._log_test(test_name, "PASS", {
                        "list_isolation": True,
                        "tenant_a_count": len(ids_a),
                        "tenant_b_count": len(ids_b),
                        "no_overlap": True
                    })
                    return True
            else:
                self._log_test(test_name, "FAIL", {
                    "error": "Could not get client lists",
                    "status_a": response_a.status_code,
                    "status_b": response_b.status_code
                })
                return False
                
        except Exception as e:
            self._log_test(test_name, "FAIL", {
                "error": f"Exception: {str(e)}"
            })
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all RLS security tests"""
        print("🔒 Running Row Level Security (RLS) Validation...")
        print(f"Target Environment: {self.results['environment']} ({self.base_url})")
        print("⚠️  CRITICAL FOR LGPD COMPLIANCE")
        print("-" * 60)
        
        # Run RLS tests
        test_results = [
            self.test_rls_isolation_core(),
            self.test_rls_bidirectional(),
            self.test_tenant_list_isolation()
        ]
        
        # Calculate overall status
        all_passed = all(test_results)
        has_critical_failures = self.results["summary"]["critical_failures"] > 0
        
        if has_critical_failures:
            self.results["overall_status"] = "CRITICAL_FAIL"
            self.results["lgpd_compliance"] = "NON_COMPLIANT"
        else:
            self.results["overall_status"] = "PASS" if all_passed else "FAIL"
            self.results["lgpd_compliance"] = "COMPLIANT" if all_passed else "UNKNOWN"
        
        print("-" * 60)
        print(f"📊 Summary: {self.results['summary']['passed']}/{self.results['summary']['total']} tests passed")
        print(f"🔴 Critical Failures: {self.results['summary']['critical_failures']}")
        print(f"🎯 Overall Status: {self.results['overall_status']}")
        print(f"📋 LGPD Compliance: {self.results['lgpd_compliance']}")
        
        if has_critical_failures:
            print("\n🚨 CRITICAL SECURITY ISSUE DETECTED!")
            print("❗ IMMEDIATE ACTION REQUIRED:")
            print("- DO NOT DEPLOY TO PRODUCTION")
            print("- Review Supabase RLS policies in supabase/policies/*.sql")
            print("- Verify tenant_id binding in all database queries")
            print("- Run unit test: tests/integration/test_rls.py")
            print("- Contact security team immediately")
        elif not all_passed:
            print("\n❗ Remediation suggestions:")
            print("- Check demo user setup (contab_a@demo.local, contab_b@demo.local)")
            print("- Verify API authentication is working correctly")
            print("- Review database connection and RLS policy implementation")
        
        return self.results


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AUDITORIA360 RLS Security Validation")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL for API testing")
    parser.add_argument("--output", help="Output JSON file for results")
    parser.add_argument("--staging", action="store_true", help="Test against staging environment")
    
    args = parser.parse_args()
    
    # Use staging URL if flag is provided  
    test_url = "https://staging.seudominio.com" if args.staging else args.url
    
    validator = RLSSecurityValidator(test_url)
    results = validator.run_all_tests()
    
    # Save results if output file specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")
    
    # Exit with appropriate code
    if results["overall_status"] == "CRITICAL_FAIL":
        print("\n🚨 Exiting with critical failure code")
        sys.exit(2)  # Critical security failure
    elif results["overall_status"] == "PASS":
        sys.exit(0)
    else:
        sys.exit(1)  # Regular failure


if __name__ == "__main__":
    main()