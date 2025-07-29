"""
Performance Test Suite for AUDITORIA360 Optimized Endpoints
Tests the performance improvements implemented for the three critical endpoints
"""

import os
import sys
import time
from unittest.mock import Mock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_mock_user():
    """Create a mock user for testing"""
    user = Mock()
    user.id = 1
    user.role = "administrador"
    user.username = "test_user"
    return user


def test_audit_relatorio_performance():
    """Test /api/v1/auditorias/relatorio endpoint performance"""
    print("🔍 Testing Audit Report Generation Performance...")

    try:
        # Import and patch the auth dependency
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        from src.api.routers.audit import router

        # Create test app with just the audit router
        test_app = FastAPI()

        # Mock the auth dependency
        def mock_get_current_user():
            return create_mock_user()

        def mock_get_db():
            return Mock()

        # Override dependencies
        test_app.dependency_overrides = {
            "get_current_user": mock_get_current_user,
            "get_db": mock_get_db,
        }

        test_app.include_router(router, prefix="/auditorias")
        client = TestClient(test_app)

        # Test different scenarios
        test_cases = [
            {
                "params": "?period_start=2024-01-01&period_end=2024-01-31",
                "name": "Monthly Report",
            },
            {"params": "?audit_id=123", "name": "Specific Audit"},
            {"params": "?format=pdf", "name": "PDF Format"},
        ]

        results = []

        for case in test_cases:
            start_time = time.time()
            response = client.get(f"/auditorias/relatorio{case['params']}")
            duration = time.time() - start_time

            results.append(
                {
                    "name": case["name"],
                    "duration": duration,
                    "status": response.status_code,
                    "target_met": duration < 1.0,
                }
            )

            print(
                f"   📊 {case['name']}: {duration:.3f}s ({'✅' if duration < 1.0 else '⚠️'})"
            )

        avg_time = sum(r["duration"] for r in results) / len(results)
        all_targets_met = all(r["target_met"] for r in results)

        print(f"   📈 Average Time: {avg_time:.3f}s")
        print(f"   🎯 Target Met (<1s): {'✅ Yes' if all_targets_met else '❌ No'}")

        return {
            "endpoint": "/api/v1/auditorias/relatorio",
            "target": "< 1s",
            "average_time": avg_time,
            "target_met": all_targets_met,
            "details": results,
        }

    except Exception as e:
        print(f"   ❌ Error testing audit report: {e}")
        return {"endpoint": "/api/v1/auditorias/relatorio", "error": str(e)}


def test_compliance_check_performance():
    """Test /api/v1/compliance/check endpoint performance"""
    print("\n🔒 Testing Compliance Check Performance...")

    try:
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        from src.api.routers.compliance import router

        # Create test app
        test_app = FastAPI()

        # Mock dependencies
        def mock_get_current_user():
            return create_mock_user()

        def mock_get_db():
            return Mock()

        test_app.dependency_overrides = {
            "get_current_user": mock_get_current_user,
            "get_db": mock_get_db,
        }

        test_app.include_router(router, prefix="/compliance")
        client = TestClient(test_app)

        # Test different entity types
        test_cases = [
            {
                "params": "?entity_type=payroll&entity_id=emp001",
                "name": "Payroll Check",
            },
            {
                "params": "?entity_type=employee&entity_id=12345",
                "name": "Employee Check",
            },
            {"params": "?entity_type=cct&entity_id=cct456", "name": "CCT Check"},
        ]

        results = []

        for case in test_cases:
            start_time = time.time()
            response = client.get(f"/compliance/check{case['params']}")
            duration = time.time() - start_time

            results.append(
                {
                    "name": case["name"],
                    "duration": duration,
                    "status": response.status_code,
                    "target_met": duration < 1.0,
                }
            )

            print(
                f"   🔍 {case['name']}: {duration:.3f}s ({'✅' if duration < 1.0 else '⚠️'})"
            )

        avg_time = sum(r["duration"] for r in results) / len(results)
        all_targets_met = all(r["target_met"] for r in results)

        print(f"   📈 Average Time: {avg_time:.3f}s")
        print(f"   🎯 Target Met (<1s): {'✅ Yes' if all_targets_met else '❌ No'}")

        return {
            "endpoint": "/api/v1/compliance/check",
            "target": "< 1s",
            "average_time": avg_time,
            "target_met": all_targets_met,
            "details": results,
        }

    except Exception as e:
        print(f"   ❌ Error testing compliance check: {e}")
        return {"endpoint": "/api/v1/compliance/check", "error": str(e)}


def test_portal_stats_performance():
    """Test portal_demandas /stats/ endpoint performance"""
    print("\n📊 Testing Portal Stats Performance...")

    try:
        from fastapi.testclient import TestClient

        from portal_demandas.api import app

        client = TestClient(app)

        # Test multiple runs to get average
        durations = []

        for i in range(5):
            start_time = time.time()
            client.get("/stats/")
            duration = time.time() - start_time
            durations.append(duration)

        avg_time = sum(durations) / len(durations)
        max_time = max(durations)
        min_time = min(durations)
        target_met = avg_time < 0.5

        print(f"   📊 Average Time: {avg_time:.3f}s")
        print(f"   📊 Min Time: {min_time:.3f}s")
        print(f"   📊 Max Time: {max_time:.3f}s")
        print(f"   🎯 Target Met (<0.5s): {'✅ Yes' if target_met else '❌ No'}")

        return {
            "endpoint": "/stats/ (portal_demandas)",
            "target": "< 0.5s",
            "average_time": avg_time,
            "target_met": target_met,
            "details": {
                "min_time": min_time,
                "max_time": max_time,
                "runs": len(durations),
            },
        }

    except Exception as e:
        print(f"   ❌ Error testing portal stats: {e}")
        return {"endpoint": "/stats/ (portal_demandas)", "error": str(e)}


def run_performance_tests():
    """Run all performance tests and generate report"""
    print("🚀 AUDITORIA360 Performance Optimization Test Suite")
    print("=" * 60)

    test_results = []

    # Run all tests
    test_results.append(test_audit_relatorio_performance())
    test_results.append(test_compliance_check_performance())
    test_results.append(test_portal_stats_performance())

    # Generate summary report
    print("\n" + "=" * 60)
    print("📋 PERFORMANCE TEST SUMMARY")
    print("=" * 60)

    total_endpoints = len(test_results)
    targets_met = sum(1 for r in test_results if r.get("target_met", False))

    for result in test_results:
        if "error" in result:
            print(f"❌ {result['endpoint']}: ERROR - {result['error']}")
        else:
            status = "✅ PASS" if result["target_met"] else "⚠️  NEEDS IMPROVEMENT"
            print(
                f"{status} {result['endpoint']}: {result['average_time']:.3f}s (target: {result['target']})"
            )

    print(
        f"\n📊 Overall Results: {targets_met}/{total_endpoints} endpoints meeting performance targets"
    )

    if targets_met == total_endpoints:
        print("🎉 ALL PERFORMANCE TARGETS MET! Optimization successful.")
    else:
        print("⚠️  Some endpoints need further optimization.")

    print("\n🔧 Optimizations Implemented:")
    print("   • Redis caching for reports and heavy queries")
    print("   • Single aggregated SQL queries instead of multiple queries")
    print("   • Reduced pagination limits (100 -> 50 items max)")
    print("   • Performance timing and monitoring")
    print("   • Fallback cache system for Redis unavailability")

    return test_results


if __name__ == "__main__":
    run_performance_tests()
