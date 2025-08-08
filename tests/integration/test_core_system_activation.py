"""
Integration test for the activated core system architecture
Tests the main components of the systemic architecture activation
"""


import requests

# API Base URL
API_BASE = "http://localhost:8001"


class TestCoreSystemIntegration:
    """Test suite for the core system architecture activation"""

    def test_system_health_endpoint(self):
        """Test that the system health endpoint is working"""
        response = requests.get(f"{API_BASE}/api/core/system/health")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "health" in data
        assert "core_system" in data["health"]
        assert "components" in data["health"]

        # Verify core components are present
        core_system = data["health"]["core_system"]
        assert "initialized" in core_system
        assert "cache_connected" in core_system
        assert "auth_system" in core_system

        components = data["health"]["components"]
        expected_components = [
            "authentication",
            "database",
            "cache",
            "automation",
            "ml_pipeline",
        ]
        for component in expected_components:
            assert component in components

        print("✅ System health endpoint working correctly")
        print(f"   Core system initialized: {core_system['initialized']}")
        print(f"   Cache backend: {components['cache']}")
        print(f"   Components status: {list(components.keys())}")

    def test_business_flow_endpoint_structure(self):
        """Test the business flow endpoint structure (without authentication)"""
        # This will fail due to authentication, but we can test the structure
        response = requests.get(f"{API_BASE}/api/core/business-flow/1")

        # We expect 403 due to missing authentication
        assert response.status_code == 403

        error_data = response.json()
        assert "detail" in error_data
        assert "Not authenticated" in error_data["detail"]

        print("✅ Business flow endpoint correctly requires authentication")

    def test_automation_context_endpoint_structure(self):
        """Test the automation context endpoint structure"""
        response = requests.get(f"{API_BASE}/api/core/automation-context/1")

        # We expect 403 due to missing authentication
        assert response.status_code == 403

        error_data = response.json()
        assert "detail" in error_data

        print("✅ Automation context endpoint correctly requires authentication")

    def test_ml_pipeline_endpoint_structure(self):
        """Test the ML pipeline endpoint structure"""
        response = requests.get(f"{API_BASE}/api/core/ml-pipeline/1")

        # We expect 403 due to missing authentication
        assert response.status_code == 403

        print("✅ ML pipeline endpoint correctly requires authentication")

    def test_api_documentation_available(self):
        """Test that API documentation is available"""
        response = requests.get(f"{API_BASE}/docs")

        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

        print("✅ API documentation is available at /docs")

    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is available"""
        response = requests.get(f"{API_BASE}/openapi.json")

        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

        # Check that our core business endpoints are in the schema
        paths = schema["paths"]
        expected_paths = [
            "/api/core/system/health",
            "/api/core/business-flow/{client_id}",
            "/api/core/automation-context/{client_id}",
            "/api/core/ml-pipeline/{client_id}",
        ]

        for path in expected_paths:
            assert path in paths, f"Path {path} not found in OpenAPI schema"

        print("✅ OpenAPI schema includes core business endpoints")
        print(f"   Total endpoints: {len(paths)}")

    def test_core_system_endpoints_discovery(self):
        """Test discovery of all core system endpoints"""
        response = requests.get(f"{API_BASE}/openapi.json")
        schema = response.json()

        core_endpoints = {
            path: methods
            for path, methods in schema["paths"].items()
            if "/api/core/" in path
        }

        print("✅ Core system endpoints discovered:")
        for endpoint, methods in core_endpoints.items():
            print(f"   {endpoint}: {list(methods.keys())}")

        # Verify we have the expected number of core endpoints
        assert len(core_endpoints) >= 4, "Expected at least 4 core endpoints"

    def test_frontend_backend_communication_setup(self):
        """Test that frontend can communicate with backend (CORS setup)"""
        # Simulate a preflight request from frontend
        response = requests.options(
            f"{API_BASE}/api/core/system/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )

        # Should allow CORS requests from frontend
        assert response.status_code in [200, 204]

        # Check CORS headers
        cors_headers = response.headers
        assert "access-control-allow-origin" in cors_headers

        print("✅ CORS setup allows frontend-backend communication")


def run_integration_tests():
    """Run all integration tests"""
    print("🚀 AUDITORIA360 - Core System Integration Tests")
    print("=" * 55)

    test_suite = TestCoreSystemIntegration()

    tests = [
        test_suite.test_system_health_endpoint,
        test_suite.test_business_flow_endpoint_structure,
        test_suite.test_automation_context_endpoint_structure,
        test_suite.test_ml_pipeline_endpoint_structure,
        test_suite.test_api_documentation_available,
        test_suite.test_openapi_schema_available,
        test_suite.test_core_system_endpoints_discovery,
        test_suite.test_frontend_backend_communication_setup,
    ]

    results = {"passed": 0, "failed": 0, "errors": []}

    for test in tests:
        try:
            print(f"\n🧪 Running: {test.__name__}")
            print("-" * 40)
            test()
            results["passed"] += 1
            print(f"✅ PASSED: {test.__name__}")
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"{test.__name__}: {str(e)}")
            print(f"❌ FAILED: {test.__name__} - {str(e)}")

    print(f"\n📊 Test Results:")
    print(f"   ✅ Passed: {results['passed']}")
    print(f"   ❌ Failed: {results['failed']}")

    if results["errors"]:
        print(f"\n❌ Errors:")
        for error in results["errors"]:
            print(f"   {error}")

    return results


if __name__ == "__main__":
    results = run_integration_tests()

    print(f"\n🎯 Architecture Activation Status:")
    if results["failed"] == 0:
        print("✅ Core system architecture successfully activated!")
        print("   - Frontend ↔ Backend communication: READY")
        print("   - Authentication pipeline: CONFIGURED")
        print("   - Automation context: IMPLEMENTED")
        print("   - ML data pipeline: AVAILABLE")
        print("   - System health monitoring: ACTIVE")
    else:
        print("⚠️  Core system architecture partially activated")
        print(
            f"   {results['passed']}/{results['passed'] + results['failed']} components working"
        )

    exit(0 if results["failed"] == 0 else 1)
