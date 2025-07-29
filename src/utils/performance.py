"""
Performance Optimization Module for AUDITORIA360
Implements bottleneck analysis, query optimization, and performance monitoring.
"""

import asyncio
import json
import logging
import threading
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

import duckdb
import psutil
import sqlalchemy
from sqlalchemy import create_engine, text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""

    function_name: str
    execution_time: float
    memory_usage_mb: float
    cpu_percent: float
    timestamp: datetime
    parameters: Optional[Dict[str, Any]] = None
    result_size: Optional[int] = None
    error: Optional[str] = None


class PerformanceProfiler:
    """Advanced performance profiler for AUDITORIA360"""

    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self._lock = threading.Lock()
        self.slow_queries_threshold = 1.0  # seconds
        self.memory_threshold = 100  # MB

    def profile_function(self, include_params: bool = False):
        """Decorator to profile function performance"""

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return self._profile_execution(func, args, kwargs, include_params)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await self._profile_async_execution(
                    func, args, kwargs, include_params
                )

            return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

        return decorator

    def _profile_execution(
        self, func: Callable, args: tuple, kwargs: dict, include_params: bool
    ):
        """Profile synchronous function execution"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        start_cpu = psutil.cpu_percent()

        try:
            result = func(*args, **kwargs)
            error = None
        except Exception as e:
            result = None
            error = str(e)
            raise
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            end_cpu = psutil.cpu_percent()

            metrics = PerformanceMetrics(
                function_name=func.__name__,
                execution_time=end_time - start_time,
                memory_usage_mb=end_memory - start_memory,
                cpu_percent=(start_cpu + end_cpu) / 2,
                timestamp=datetime.now(),
                parameters=(
                    {"args_count": len(args), "kwargs_keys": list(kwargs.keys())}
                    if include_params
                    else None
                ),
                result_size=len(result) if hasattr(result, "__len__") else None,
                error=error,
            )

            self._record_metrics(metrics)

        return result

    async def _profile_async_execution(
        self, func: Callable, args: tuple, kwargs: dict, include_params: bool
    ):
        """Profile asynchronous function execution"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        start_cpu = psutil.cpu_percent()

        try:
            result = await func(*args, **kwargs)
            error = None
        except Exception as e:
            result = None
            error = str(e)
            raise
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            end_cpu = psutil.cpu_percent()

            metrics = PerformanceMetrics(
                function_name=func.__name__,
                execution_time=end_time - start_time,
                memory_usage_mb=end_memory - start_memory,
                cpu_percent=(start_cpu + end_cpu) / 2,
                timestamp=datetime.now(),
                parameters=(
                    {"args_count": len(args), "kwargs_keys": list(kwargs.keys())}
                    if include_params
                    else None
                ),
                result_size=len(result) if hasattr(result, "__len__") else None,
                error=error,
            )

            self._record_metrics(metrics)

        return result

    def _record_metrics(self, metrics: PerformanceMetrics):
        """Thread-safe metrics recording"""
        with self._lock:
            self.metrics.append(metrics)

            # Log slow operations
            if metrics.execution_time > self.slow_queries_threshold:
                logger.warning(
                    f"Slow operation detected: {metrics.function_name} took {metrics.execution_time:.2f}s"
                )

            # Log high memory usage
            if metrics.memory_usage_mb > self.memory_threshold:
                logger.warning(
                    f"High memory usage: {metrics.function_name} used {metrics.memory_usage_mb:.2f}MB"
                )

    def get_bottlenecks(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks in the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]

        # Group by function
        function_stats = {}
        for metric in recent_metrics:
            if metric.function_name not in function_stats:
                function_stats[metric.function_name] = {
                    "total_calls": 0,
                    "total_time": 0,
                    "avg_time": 0,
                    "max_time": 0,
                    "total_memory": 0,
                    "avg_memory": 0,
                    "max_memory": 0,
                    "error_count": 0,
                }

            stats = function_stats[metric.function_name]
            stats["total_calls"] += 1
            stats["total_time"] += metric.execution_time
            stats["max_time"] = max(stats["max_time"], metric.execution_time)
            stats["total_memory"] += metric.memory_usage_mb
            stats["max_memory"] = max(stats["max_memory"], metric.memory_usage_mb)

            if metric.error:
                stats["error_count"] += 1

        # Calculate averages and identify bottlenecks
        bottlenecks = []
        for func_name, stats in function_stats.items():
            stats["avg_time"] = stats["total_time"] / stats["total_calls"]
            stats["avg_memory"] = stats["total_memory"] / stats["total_calls"]

            # Identify as bottleneck if:
            # 1. Average execution time > threshold
            # 2. High memory usage
            # 3. Error rate > 5%
            if (
                stats["avg_time"] > self.slow_queries_threshold
                or stats["avg_memory"] > self.memory_threshold
                or (stats["error_count"] / stats["total_calls"]) > 0.05
            ):

                bottlenecks.append(
                    {
                        "function_name": func_name,
                        "severity": self._calculate_severity(stats),
                        "stats": stats,
                        "recommendations": self._get_recommendations(func_name, stats),
                    }
                )

        return sorted(bottlenecks, key=lambda x: x["severity"], reverse=True)

    def _calculate_severity(self, stats: Dict[str, Any]) -> float:
        """Calculate bottleneck severity score (0-100)"""
        severity = 0

        # Time-based severity
        if stats["avg_time"] > self.slow_queries_threshold:
            severity += min(40, (stats["avg_time"] / self.slow_queries_threshold) * 20)

        # Memory-based severity
        if stats["avg_memory"] > self.memory_threshold:
            severity += min(30, (stats["avg_memory"] / self.memory_threshold) * 15)

        # Error-based severity
        error_rate = stats["error_count"] / stats["total_calls"]
        if error_rate > 0:
            severity += min(30, error_rate * 100)

        return min(100, severity)

    def _get_recommendations(self, func_name: str, stats: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        if stats["avg_time"] > self.slow_queries_threshold:
            recommendations.append("Consider optimizing algorithm or adding caching")
            if "database" in func_name.lower() or "query" in func_name.lower():
                recommendations.append(
                    "Review database query performance and add indexes"
                )

        if stats["avg_memory"] > self.memory_threshold:
            recommendations.append(
                "Optimize memory usage - consider streaming or pagination"
            )
            recommendations.append(
                "Review data structures and remove unnecessary object creation"
            )

        if stats["error_count"] > 0:
            recommendations.append("Add better error handling and validation")
            recommendations.append("Review input parameters and edge cases")

        return recommendations


class DatabaseOptimizer:
    """Database query optimization utilities"""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url
        self.query_cache = {}
        self.query_stats = {}

    @contextmanager
    def profile_query(self, query_name: str):
        """Context manager to profile database queries"""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024

        try:
            yield
        finally:
            execution_time = time.time() - start_time
            memory_used = (
                psutil.Process().memory_info().rss / 1024 / 1024 - start_memory
            )

            if query_name not in self.query_stats:
                self.query_stats[query_name] = []

            self.query_stats[query_name].append(
                {
                    "execution_time": execution_time,
                    "memory_usage": memory_used,
                    "timestamp": datetime.now(),
                }
            )

            if execution_time > 1.0:  # Log slow queries
                logger.warning(
                    f"Slow query detected: {query_name} took {execution_time:.2f}s"
                )

    def optimize_postgresql_query(self, query: str) -> Dict[str, Any]:
        """Analyze and optimize PostgreSQL queries"""
        optimizations = {"query": query, "suggestions": [], "estimated_improvement": 0}

        query_lower = query.lower()

        # Check for missing indexes
        if "where" in query_lower and "index" not in query_lower:
            optimizations["suggestions"].append(
                "Consider adding indexes on WHERE clause columns"
            )
            optimizations["estimated_improvement"] += 30

        # Check for SELECT *
        if "select *" in query_lower:
            optimizations["suggestions"].append(
                "Avoid SELECT * - specify only needed columns"
            )
            optimizations["estimated_improvement"] += 20

        # Check for JOIN optimization
        if "join" in query_lower and "on" in query_lower:
            optimizations["suggestions"].append(
                "Ensure JOIN conditions use indexed columns"
            )
            optimizations["estimated_improvement"] += 25

        # Check for ORDER BY without LIMIT
        if "order by" in query_lower and "limit" not in query_lower:
            optimizations["suggestions"].append(
                "Consider adding LIMIT to ORDER BY queries"
            )
            optimizations["estimated_improvement"] += 15

        return optimizations

    def optimize_duckdb_query(self, query: str) -> Dict[str, Any]:
        """Analyze and optimize DuckDB queries"""
        optimizations = {"query": query, "suggestions": [], "estimated_improvement": 0}

        query_lower = query.lower()

        # Check for efficient file formats
        if "csv" in query_lower:
            optimizations["suggestions"].append(
                "Consider using Parquet format for better performance"
            )
            optimizations["estimated_improvement"] += 40

        # Check for column projection
        if "select *" in query_lower:
            optimizations["suggestions"].append(
                "Project only necessary columns for better I/O performance"
            )
            optimizations["estimated_improvement"] += 25

        # Check for filter pushdown
        if "where" in query_lower:
            optimizations["suggestions"].append(
                "Ensure filters are applied early (filter pushdown)"
            )
            optimizations["estimated_improvement"] += 20

        return optimizations

    def get_slow_queries(
        self, threshold: float = 1.0, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get slowest queries above threshold"""
        slow_queries = []

        for query_name, stats_list in self.query_stats.items():
            avg_time = sum(s["execution_time"] for s in stats_list) / len(stats_list)
            max_time = max(s["execution_time"] for s in stats_list)

            if avg_time > threshold:
                slow_queries.append(
                    {
                        "query_name": query_name,
                        "avg_execution_time": avg_time,
                        "max_execution_time": max_time,
                        "call_count": len(stats_list),
                        "total_time": sum(s["execution_time"] for s in stats_list),
                    }
                )

        return sorted(
            slow_queries, key=lambda x: x["avg_execution_time"], reverse=True
        )[:limit]


class CacheManager:
    """Intelligent caching system for performance optimization"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache = {}
        self.access_times = {}
        self.creation_times = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get cached value with TTL check"""
        with self._lock:
            if key in self.cache:
                # Check TTL
                if time.time() - self.creation_times[key] > self.ttl_seconds:
                    self._remove_key(key)
                    return None

                self.access_times[key] = time.time()
                return self.cache[key]
            return None

    def set(self, key: str, value: Any) -> None:
        """Set cached value with LRU eviction"""
        with self._lock:
            current_time = time.time()

            # Remove expired entries
            self._cleanup_expired()

            # Check if we need to evict
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict_lru()

            self.cache[key] = value
            self.access_times[key] = current_time
            self.creation_times[key] = current_time

    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [
            key
            for key, creation_time in self.creation_times.items()
            if current_time - creation_time > self.ttl_seconds
        ]

        for key in expired_keys:
            self._remove_key(key)

    def _evict_lru(self):
        """Evict least recently used entry"""
        if not self.access_times:
            return

        lru_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        self._remove_key(lru_key)

    def _remove_key(self, key: str):
        """Remove key from all dictionaries"""
        self.cache.pop(key, None)
        self.access_times.pop(key, None)
        self.creation_times.pop(key, None)

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": self._calculate_hit_rate(),
            "memory_usage_mb": self._estimate_memory_usage(),
        }

    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate (simplified)"""
        # This is a simplified implementation
        # In a real system, you'd track hits and misses
        return 0.75  # Placeholder

    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage in MB"""
        # Rough estimation based on number of objects
        return len(self.cache) * 0.001  # ~1KB per entry estimate


# Global performance profiler instance
profiler = PerformanceProfiler()


# Decorator shortcuts
def profile(include_params: bool = False):
    """Convenient decorator for profiling functions"""
    return profiler.profile_function(include_params=include_params)


def profile_database_query(query_name: str):
    """Decorator for profiling database queries"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db_optimizer = DatabaseOptimizer()
            with db_optimizer.profile_query(query_name):
                return func(*args, **kwargs)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            db_optimizer = DatabaseOptimizer()
            with db_optimizer.profile_query(query_name):
                return await func(*args, **kwargs)

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator


# Cache instance
cache = CacheManager()


def cached(ttl_seconds: int = 3600, key_func: Optional[Callable] = None):
    """Decorator for caching function results"""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            return result

        return wrapper

    return decorator
