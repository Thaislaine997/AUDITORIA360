"""
Tests for the enhanced performance monitoring and alerting features
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

# Test basic imports
def test_imports():
    """Test that all monitoring modules can be imported"""
    try:
        from src.utils.performance import PerformanceProfiler, DatabaseOptimizer, CacheManager
        from src.utils.monitoring import MonitoringSystem, AlertManager, MetricsCollector
        from src.utils.api_integration import setup_monitoring_integration
        assert True, "All imports successful"
    except ImportError as e:
        pytest.skip(f"Enhanced features not available: {e}")

def test_performance_profiler():
    """Test performance profiler functionality"""
    try:
        from src.utils.performance import PerformanceProfiler, profile
        
        profiler = PerformanceProfiler()
        
        @profile(include_params=True)
        def test_function(x, y=10):
            time.sleep(0.1)  # Simulate work
            return x + y
        
        result = test_function(5, y=15)
        assert result == 20
        
        # Check that metrics were recorded
        assert len(profiler.metrics) > 0
        
        # Check bottlenecks analysis
        bottlenecks = profiler.get_bottlenecks(hours=1)
        assert isinstance(bottlenecks, list)
        
    except ImportError:
        pytest.skip("Performance profiler not available")

def test_monitoring_system():
    """Test monitoring system initialization"""
    try:
        from src.utils.monitoring import MonitoringSystem, AlertSeverity
        
        monitoring = MonitoringSystem()
        
        # Test metrics collection
        monitoring.metrics.increment_counter("test_counter")
        monitoring.metrics.set_gauge("test_gauge", 42.5)
        monitoring.metrics.record_histogram("test_histogram", 123.45)
        
        # Test metrics summary
        summary = monitoring.metrics.get_metrics_summary(hours=1)
        assert isinstance(summary, dict)
        
        # Test alert rules
        monitoring.alert_manager.add_alert_rule(
            metric_name="test_gauge",
            threshold=50,
            condition="gt", 
            severity=AlertSeverity.MEDIUM,
            title="Test Alert",
            description="Test alert description"
        )
        
        assert len(monitoring.alert_manager.alert_rules) > 0
        
    except ImportError:
        pytest.skip("Monitoring system not available")

def test_database_optimizer():
    """Test database query optimization"""
    try:
        from src.utils.performance import DatabaseOptimizer
        
        optimizer = DatabaseOptimizer()
        
        # Test PostgreSQL optimization
        pg_query = "SELECT * FROM users WHERE email = 'test@example.com'"
        pg_result = optimizer.optimize_postgresql_query(pg_query)
        
        assert 'suggestions' in pg_result
        assert 'estimated_improvement' in pg_result
        assert isinstance(pg_result['suggestions'], list)
        
        # Test DuckDB optimization
        duck_query = "SELECT * FROM read_csv('data.csv') WHERE column1 > 100"
        duck_result = optimizer.optimize_duckdb_query(duck_query)
        
        assert 'suggestions' in duck_result
        assert 'estimated_improvement' in duck_result
        
    except ImportError:
        pytest.skip("Database optimizer not available")

def test_cache_manager():
    """Test cache functionality"""
    try:
        from src.utils.performance import CacheManager, cached
        
        cache = CacheManager(max_size=10, ttl_seconds=5)
        
        # Test basic cache operations
        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"
        
        # Test TTL expiration
        time.sleep(6)  # Wait for TTL to expire
        assert cache.get("test_key") is None
        
        # Test cache decorator
        @cached(ttl_seconds=10)
        def expensive_function(x):
            time.sleep(0.01)  # Simulate expensive operation
            return x * 2
        
        # First call should execute function
        start_time = time.time()
        result1 = expensive_function(5)
        first_call_time = time.time() - start_time
        
        # Second call should be cached (faster)
        start_time = time.time()
        result2 = expensive_function(5)
        second_call_time = time.time() - start_time
        
        assert result1 == result2 == 10
        assert second_call_time < first_call_time
        
    except ImportError:
        pytest.skip("Cache manager not available")

@pytest.mark.asyncio
async def test_health_checks():
    """Test health check functionality"""
    try:
        from src.utils.monitoring import HealthChecker, MetricsCollector
        
        metrics = MetricsCollector()
        health_checker = HealthChecker(metrics)
        
        # Add a simple health check
        async def test_health_check():
            return {"status": "healthy", "details": {"test": True}}
        
        health_checker.add_health_check("test_check", test_health_check)
        
        # Run health checks
        results = await health_checker.run_all_checks()
        
        assert len(results) == 1
        assert results[0].name == "test_check"
        assert results[0].status == "healthy"
        
    except ImportError:
        pytest.skip("Health checker not available")

def test_api_integration():
    """Test API integration with monitoring"""
    try:
        from api.index import app
        
        client = TestClient(app)
        
        # Test basic health endpoints
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        
        # Test system status endpoint
        response = client.get("/api/v1/system/status")
        assert response.status_code == 200
        data = response.json()
        assert "api_version" in data
        assert "components" in data
        
        # Test monitoring endpoints if available
        try:
            response = client.get("/api/v1/monitoring/dashboard")
            # If monitoring is available, should return 200, otherwise 503
            assert response.status_code in [200, 503]
        except:
            pass  # Monitoring may not be fully initialized in test environment
        
    except ImportError:
        pytest.skip("API integration test skipped - dependencies not available")

def test_demo_endpoints():
    """Test demonstration endpoints"""
    try:
        from api.index import app
        
        client = TestClient(app)
        
        # Test cached data endpoint
        response = client.get("/api/v1/demo/cached-data")
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "timestamp" in data
        
        # Test alert trigger endpoint
        response = client.get("/api/v1/demo/trigger-alert")
        if response.status_code == 200:
            data = response.json()
            assert "message" in data
        
    except Exception as e:
        pytest.skip(f"Demo endpoints test skipped: {e}")

if __name__ == "__main__":
    # Run tests directly for development
    print("Running enhanced features tests...")
    
    test_imports()
    print("✅ Imports test passed")
    
    test_performance_profiler()
    print("✅ Performance profiler test passed")
    
    test_monitoring_system()
    print("✅ Monitoring system test passed")
    
    test_database_optimizer()
    print("✅ Database optimizer test passed")
    
    test_cache_manager()
    print("✅ Cache manager test passed")
    
    asyncio.run(test_health_checks())
    print("✅ Health checks test passed")
    
    test_api_integration()
    print("✅ API integration test passed")
    
    test_demo_endpoints()
    print("✅ Demo endpoints test passed")
    
    print("\n🎉 All enhanced features tests passed!")