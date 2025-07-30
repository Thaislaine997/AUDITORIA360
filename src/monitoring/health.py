"""
Health checking system for AUDITORIA360 monitoring
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .metrics import MetricsCollector

logger = logging.getLogger(__name__)


@dataclass
class HealthCheck:
    """Health check result structure"""
    name: str
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: datetime
    response_time_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class HealthChecker:
    """Manages and executes health checks"""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.health_checks: Dict[str, Dict[str, Any]] = {}
        self.last_results: Dict[str, HealthCheck] = {}

    def add_health_check(self, name: str, check_func: Callable, interval: int = 60):
        """Add a health check function"""
        self.health_checks[name] = {
            "func": check_func,
            "interval": interval,
            "last_run": 0,
        }

    async def run_all_checks(self) -> List[HealthCheck]:
        """Run all registered health checks"""
        results = []
        current_time = time.time()

        for name, check in self.health_checks.items():
            # Check if it's time to run this check
            if current_time - check["last_run"] >= check["interval"]:
                result = await self._run_check(check)
                result.name = name
                results.append(result)
                self.last_results[name] = result
                check["last_run"] = current_time

                # Record metrics
                status_value = 1 if result.status == "healthy" else 0
                self.metrics_collector.set_gauge(
                    f"health_check_{name}_status", status_value
                )
                self.metrics_collector.set_gauge(
                    f"health_check_{name}_response_time", result.response_time_ms
                )

        return results

    async def _run_check(self, check: Dict[str, Any]) -> HealthCheck:
        """Run a single health check"""
        start_time = time.time()
        
        try:
            # Run the check function
            if asyncio.iscoroutinefunction(check["func"]):
                result = await check["func"]()
            else:
                result = check["func"]()
            
            response_time = (time.time() - start_time) * 1000

            # Parse result
            if isinstance(result, dict):
                status = result.get("status", "healthy")
                details = result.get("details", {})
                error = result.get("error")
            elif isinstance(result, bool):
                status = "healthy" if result else "unhealthy"
                details = {}
                error = None
            else:
                status = "healthy"
                details = {"result": str(result)}
                error = None

            return HealthCheck(
                name="",  # Will be set by caller
                status=status,
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details=details,
                error=error,
            )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logger.error(f"Health check failed: {e}")
            
            return HealthCheck(
                name="",  # Will be set by caller
                status="unhealthy",
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={},
                error=str(e),
            )

    def get_latest_results(self) -> Dict[str, HealthCheck]:
        """Get the latest health check results"""
        return self.last_results.copy()

    def get_overall_health(self) -> str:
        """Get overall system health status"""
        if not self.last_results:
            return "unknown"

        statuses = [result.status for result in self.last_results.values()]
        
        if all(status == "healthy" for status in statuses):
            return "healthy"
        elif any(status == "unhealthy" for status in statuses):
            return "unhealthy"
        else:
            return "degraded"