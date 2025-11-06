"""
Caching system for improved performance.
"""

import time
import hashlib
import json
from typing import Any, Optional, Callable
from functools import wraps
from cachetools import TTLCache
from .config import config
from .logging_config import get_logger
from .exceptions import CacheError

logger = get_logger(__name__)


class CacheManager:
    """Manages caching for expensive operations."""

    def __init__(self):
        cache_enabled = config.get('cache.enabled', True)
        ttl = config.get('cache.ttl', 3600)
        max_size = config.get('cache.max_size', 100)

        if cache_enabled:
            self._cache = TTLCache(maxsize=max_size, ttl=ttl)
            logger.info(f"Cache initialized: max_size={max_size}, ttl={ttl}s")
        else:
            self._cache = None
            logger.info("Cache disabled")

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache."""
        if self._cache is None:
            return None

        try:
            value = self._cache.get(key)
            if value is not None:
                logger.debug(f"Cache hit: {key}")
            return value
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any):
        """Set item in cache."""
        if self._cache is None:
            return

        try:
            self._cache[key] = value
            logger.debug(f"Cache set: {key}")
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def delete(self, key: str):
        """Delete item from cache."""
        if self._cache is None:
            return

        try:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Cache delete: {key}")
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

    def clear(self):
        """Clear all cache."""
        if self._cache is not None:
            self._cache.clear()
            logger.info("Cache cleared")

    def get_stats(self) -> dict:
        """Get cache statistics."""
        if self._cache is None:
            return {'enabled': False}

        return {
            'enabled': True,
            'size': len(self._cache),
            'maxsize': self._cache.maxsize,
            'ttl': self._cache.ttl,
        }

    @staticmethod
    def generate_key(*args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()


# Global cache instance
cache_manager = CacheManager()


def cached(ttl: Optional[int] = None):
    """
    Decorator for caching function results.

    Args:
        ttl: Time to live in seconds (uses config default if None)

    Example:
        @cached(ttl=3600)
        def expensive_function(arg1, arg2):
            # expensive computation
            return result
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__module__}.{func.__name__}:{cache_manager.generate_key(*args, **kwargs)}"

            # Try to get from cache
            result = cache_manager.get(cache_key)
            if result is not None:
                return result

            # Compute and cache
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time

            logger.debug(f"{func.__name__} took {elapsed:.2f}s")

            cache_manager.set(cache_key, result)
            return result

        return wrapper
    return decorator


def cache_clear():
    """Clear all cache. Useful for testing."""
    cache_manager.clear()
