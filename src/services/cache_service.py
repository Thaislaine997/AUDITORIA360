"""
Redis Cache Service for AUDITORIA360
Performance optimization for reports and heavy queries
"""

import json
import logging
import os
from functools import wraps
from typing import Any, Optional

import redis

logger = logging.getLogger(__name__)


class CacheService:
    """Redis-based caching service for performance optimization"""

    def __init__(self):
        """Initialize Redis connection with fallback to in-memory cache"""
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = None
        self.in_memory_cache = {}  # Fallback cache

        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info("✅ Redis cache connected successfully")
            self.cache_backend = "redis"
        except (redis.ConnectionError, redis.TimeoutError) as e:
            logger.warning(f"⚠️  Redis not available, using in-memory cache: {e}")
            self.cache_backend = "memory"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.cache_backend == "redis" and self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                return self.in_memory_cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> bool:
        """Set value in cache with TTL"""
        try:
            if self.cache_backend == "redis" and self.redis_client:
                return self.redis_client.setex(
                    key, ttl_seconds, json.dumps(value, default=str)
                )
            else:
                # Simple in-memory cache without TTL for fallback
                self.in_memory_cache[key] = value
                return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if self.cache_backend == "redis" and self.redis_client:
                return bool(self.redis_client.delete(key))
            else:
                return bool(self.in_memory_cache.pop(key, None))
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            if self.cache_backend == "redis" and self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
                return 0
            else:
                # Pattern matching for in-memory cache
                keys_to_delete = [
                    k
                    for k in self.in_memory_cache.keys()
                    if pattern.replace("*", "") in k
                ]
                for key in keys_to_delete:
                    del self.in_memory_cache[key]
                return len(keys_to_delete)
        except Exception as e:
            logger.error(f"Cache clear pattern error for {pattern}: {e}")
            return 0

    def invalidate_reports_cache(self):
        """Invalidate all report-related caches"""
        patterns = ["report:*", "audit:report:*", "compliance:report:*", "stats:*"]

        total_cleared = 0
        for pattern in patterns:
            total_cleared += self.clear_pattern(pattern)

        logger.info(f"Invalidated {total_cleared} report cache entries")
        return total_cleared


# Global cache instance
cache_service = CacheService()


def cached_response(key_prefix: str, ttl_seconds: int = 300):
    """Decorator for caching API responses"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and parameters
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache first
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_result

            # Execute function and cache result
            logger.debug(f"Cache miss for {cache_key}, executing function")
            result = await func(*args, **kwargs)

            # Cache the result
            cache_service.set(cache_key, result, ttl_seconds)
            return result

        return wrapper

    return decorator


def cached_query(key_prefix: str, ttl_seconds: int = 300):
    """Decorator for caching database query results"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"query:{key_prefix}:{hash(str(args) + str(kwargs))}"

            # Try cache first
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Query cache hit for {cache_key}")
                return cached_result

            # Execute query and cache
            result = func(*args, **kwargs)
            cache_service.set(cache_key, result, ttl_seconds)
            logger.debug(f"Query result cached for {cache_key}")
            return result

        return wrapper

    return decorator


# Cache key generators for common patterns
class CacheKeys:
    """Standard cache key patterns for the application"""

    @staticmethod
    def audit_report(audit_id: Optional[int] = None, period: str = None) -> str:
        if audit_id:
            return f"audit:report:{audit_id}"
        elif period:
            return f"audit:report:period:{period}"
        else:
            return f"audit:report:latest"

    @staticmethod
    def compliance_check(entity_type: str, entity_id: str) -> str:
        return f"compliance:check:{entity_type}:{entity_id}"

    @staticmethod
    def portal_stats(filters: str = None) -> str:
        if filters:
            return f"stats:portal:{hash(filters)}"
        else:
            return "stats:portal:all"

    @staticmethod
    def query_result(table: str, conditions: str = None) -> str:
        if conditions:
            return f"query:{table}:{hash(conditions)}"
        else:
            return f"query:{table}:all"
