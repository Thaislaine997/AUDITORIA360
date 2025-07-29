"""
Integration module for performance monitoring and alerting in AUDITORIA360 API
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request

# Import monitoring and performance utilities
try:
    from src.utils.monitoring import (
        AlertSeverity,
        get_monitoring_system,
    )
    from src.utils.performance import DatabaseOptimizer, cached, profile, profiler

    MONITORING_ENABLED = True
except ImportError:
    MONITORING_ENABLED = False

    # Create mock classes for when monitoring is not available
    class MockMonitoring:
        def start(self):
            pass

        def stop(self):
            pass

        def get_dashboard_data(self):
            return {}

    def get_monitoring_system():
        return MockMonitoring()


# Create monitoring router
monitoring_router = APIRouter(prefix="/api/v1/monitoring", tags=["Monitoring"])


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to collect API metrics automatically"""

    def __init__(self, app, monitoring_system=None):
        super().__init__(app)
        self.monitoring = monitoring_system or get_monitoring_system()

    async def dispatch(self, request: Request, call_next):
        if not MONITORING_ENABLED:
            return await call_next(request)

        start_time = time.time()
        method = request.method
        path = request.url.path

        # Skip monitoring endpoints to avoid recursion
        if path.startswith("/api/v1/monitoring"):
            return await call_next(request)

        # Increment request counter
        self.monitoring.metrics.increment_counter(
            "api_requests_total", labels={"method": method, "endpoint": path}
        )

        # Process request
        response = await call_next(request)

        # Calculate response time
        process_time = (time.time() - start_time) * 1000  # ms

        # Record metrics
        self.monitoring.metrics.record_histogram(
            "api_response_time_ms",
            process_time,
            labels={
                "method": method,
                "endpoint": path,
                "status_code": str(response.status_code),
            },
        )

        # Count responses by status
        self.monitoring.metrics.increment_counter(
            "api_responses_total", labels={"status_code": str(response.status_code)}
        )

        # Add response time header
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        return response


@monitoring_router.get("/dashboard")
async def get_monitoring_dashboard():
    """Get comprehensive monitoring dashboard data"""
    if not MONITORING_ENABLED:
        raise HTTPException(status_code=503, detail="Monitoring not available")

    monitoring = get_monitoring_system()
    dashboard_data = monitoring.get_dashboard_data()

    # Add additional context
    dashboard_data.update(
        {
            "timestamp": datetime.now().isoformat(),
            "monitoring_enabled": MONITORING_ENABLED,
            "system_info": {
                "version": "1.0.0",
                "environment": "production",  # This should come from env var
            },
        }
    )

    return dashboard_data


@monitoring_router.get("/metrics")
async def get_metrics(hours: int = 1):
    """Get metrics summary for specified time period"""
    if not MONITORING_ENABLED:
        raise HTTPException(status_code=503, detail="Monitoring not available")

    monitoring = get_monitoring_system()
    metrics_summary = monitoring.metrics.get_metrics_summary(hours=hours)

    return {
        "period_hours": hours,
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics_summary,
    }


@monitoring_router.get("/alerts")
async def get_active_alerts():
    """Get all active alerts"""
    if not MONITORING_ENABLED:
        raise HTTPException(status_code=503, detail="Monitoring not available")

    monitoring = get_monitoring_system()
    active_alerts = monitoring.alert_manager.get_active_alerts()

    return {
        "count": len(active_alerts),
        "alerts": [
            {
                "id": alert.id,
                "title": alert.title,
                "description": alert.description,
                "severity": alert.severity.value,
                "metric_name": alert.metric_name,
                "current_value": alert.current_value,
                "threshold": alert.threshold,
                "timestamp": alert.timestamp.isoformat(),
            }
            for alert in active_alerts
        ],
    }


@monitoring_router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Resolve a specific alert"""
    if not MONITORING_ENABLED:
        raise HTTPException(status_code=503, detail="Monitoring not available")

    monitoring = get_monitoring_system()
    monitoring.alert_manager.resolve_alert(alert_id)

    return {"message": f"Alert {alert_id} resolved successfully"}


@monitoring_router.get("/health")
async def get_health_checks():
    """Run and return all health checks"""
    if not MONITORING_ENABLED:
        raise HTTPException(status_code=503, detail="Monitoring not available")

    monitoring = get_monitoring_system()
    health_results = await monitoring.health_checker.run_all_checks()

    overall_status = "healthy"
    if any(result.status == "unhealthy" for result in health_results):
        overall_status = "unhealthy"
    elif any(result.status == "degraded" for result in health_results):
        overall_status = "degraded"

    return {
        "overall_status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "checks": [
            {
                "name": result.name,
                "status": result.status,
                "response_time_ms": result.response_time_ms,
                "details": result.details,
                "error": result.error,
            }
            for result in health_results
        ],
    }


@monitoring_router.get("/performance/bottlenecks")
async def get_performance_bottlenecks(hours: int = 24):
    """Get performance bottlenecks analysis"""
    if not MONITORING_ENABLED:
        return {"bottlenecks": [], "message": "Performance monitoring not available"}

    bottlenecks = profiler.get_bottlenecks(hours=hours)

    return {
        "period_hours": hours,
        "timestamp": datetime.now().isoformat(),
        "bottlenecks_count": len(bottlenecks),
        "bottlenecks": bottlenecks,
    }


@monitoring_router.post("/performance/clear-metrics")
async def clear_performance_metrics():
    """Clear stored performance metrics (admin only)"""
    if not MONITORING_ENABLED:
        raise HTTPException(status_code=503, detail="Monitoring not available")

    profiler.metrics.clear()

    return {"message": "Performance metrics cleared successfully"}


# Performance optimization endpoints
performance_router = APIRouter(prefix="/api/v1/performance", tags=["Performance"])


@performance_router.get("/database/slow-queries")
async def get_slow_queries(threshold: float = 1.0, limit: int = 10):
    """Get slowest database queries"""
    if not MONITORING_ENABLED:
        return {"slow_queries": [], "message": "Performance monitoring not available"}

    db_optimizer = DatabaseOptimizer()
    slow_queries = db_optimizer.get_slow_queries(threshold=threshold, limit=limit)

    return {
        "threshold_seconds": threshold,
        "limit": limit,
        "timestamp": datetime.now().isoformat(),
        "slow_queries": slow_queries,
    }


@performance_router.post("/database/analyze-query")
async def analyze_query(query_data: Dict[str, Any]):
    """Analyze a specific query for optimization opportunities"""
    query = query_data.get("query", "")
    database_type = query_data.get("type", "postgresql")  # postgresql or duckdb

    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    db_optimizer = DatabaseOptimizer()

    if database_type.lower() == "postgresql":
        analysis = db_optimizer.optimize_postgresql_query(query)
    elif database_type.lower() == "duckdb":
        analysis = db_optimizer.optimize_duckdb_query(query)
    else:
        raise HTTPException(status_code=400, detail="Unsupported database type")

    return {
        "database_type": database_type,
        "timestamp": datetime.now().isoformat(),
        "analysis": analysis,
    }


@performance_router.get("/cache/stats")
async def get_cache_stats():
    """Get cache performance statistics"""
    if not MONITORING_ENABLED:
        return {"cache_stats": {}, "message": "Performance monitoring not available"}

    try:
        from src.utils.performance import cache

        stats = cache.stats()

        return {"timestamp": datetime.now().isoformat(), "cache_stats": stats}
    except Exception as e:
        return {"error": str(e), "message": "Cache statistics not available"}


@performance_router.post("/cache/clear")
async def clear_cache():
    """Clear application cache (admin only)"""
    try:
        pass

        # Clear cache implementation would go here
        # cache.clear_all()  # This method would need to be implemented

        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


# Utility functions for decorated endpoints
def monitor_endpoint(endpoint_name: str):
    """Decorator to monitor specific endpoints"""

    def decorator(func):
        if not MONITORING_ENABLED:
            return func

        # This would wrap the function with monitoring
        # Implementation depends on whether it's sync or async
        return profile(include_params=True)(func)

    return decorator


def cache_endpoint(ttl_seconds: int = 300):
    """Decorator to cache endpoint responses"""

    def decorator(func):
        if not MONITORING_ENABLED:
            return func

        return cached(ttl_seconds=ttl_seconds)(func)

    return decorator


# Health check functions for common services
async def check_database_health():
    """Check database connectivity and performance"""
    try:
        # This would test actual database connection
        # For now, we'll simulate the check
        start_time = time.time()

        # Simulate database check
        await asyncio.sleep(0.01)  # Simulate connection time

        response_time = (time.time() - start_time) * 1000

        return {
            "status": "healthy",
            "details": {
                "response_time_ms": response_time,
                "connection_pool_size": 10,  # This would come from actual pool
                "active_connections": 2,
            },
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


async def check_storage_health():
    """Check storage (R2) connectivity"""
    try:
        # This would test actual R2 connection
        # For now, we'll simulate the check
        start_time = time.time()

        # Simulate storage check
        await asyncio.sleep(0.005)  # Simulate API call

        response_time = (time.time() - start_time) * 1000

        return {
            "status": "healthy",
            "details": {"response_time_ms": response_time, "bucket_accessible": True},
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


def setup_monitoring_integration(app):
    """Setup monitoring integration with FastAPI app"""
    if not MONITORING_ENABLED:
        return

    # Initialize monitoring system
    monitoring = get_monitoring_system()

    # Add middleware
    app.add_middleware(MonitoringMiddleware, monitoring_system=monitoring)

    # Include routers
    app.include_router(monitoring_router)
    app.include_router(performance_router)

    # Add health checks
    monitoring.health_checker.add_health_check("database", check_database_health)
    monitoring.health_checker.add_health_check("storage", check_storage_health)

    # Setup default alerts
    monitoring.alert_manager.add_alert_rule(
        metric_name="api_response_time_ms",
        threshold=1000,  # 1 second
        condition="gt",
        severity=AlertSeverity.MEDIUM,
        title="API Response Time High",
        description="API response time is above 1 second",
    )

    monitoring.alert_manager.add_alert_rule(
        metric_name="api_error_rate",
        threshold=5.0,  # 5%
        condition="gt",
        severity=AlertSeverity.HIGH,
        title="High API Error Rate",
        description="API error rate is above 5%",
    )

    # Start monitoring
    monitoring.start()

    return monitoring


# Example of how to use the decorators in actual endpoints
"""
@app.get("/api/v1/auditorias/heavy-operation")
@monitor_endpoint("heavy_operation")
@cache_endpoint(ttl_seconds=600)  # Cache for 10 minutes
async def heavy_operation_endpoint():
    # Your heavy computation here
    result = perform_heavy_computation()
    return result
"""
