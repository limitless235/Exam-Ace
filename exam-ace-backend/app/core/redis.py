"""
Async Redis client wrapper.
Gracefully degrades if Redis is not available (logs warning, skips operations).
"""
from __future__ import annotations

import logging
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)

_redis: aioredis.Redis | None = None
_available: bool = False


async def init_redis(url: str) -> None:
    """Connect to Redis.  If connection fails, log and continue (graceful degradation)."""
    global _redis, _available
    try:
        _redis = aioredis.from_url(url, decode_responses=True)
        await _redis.ping()
        _available = True
        logger.info("Redis connected at %s", url)
    except Exception as exc:
        _available = False
        logger.warning("Redis unavailable (%s) — rate limiting disabled.", exc)


async def close_redis() -> None:
    global _redis, _available
    if _redis is not None:
        await _redis.aclose()
        _redis = None
        _available = False


def get_redis() -> aioredis.Redis | None:
    return _redis if _available else None


def is_available() -> bool:
    return _available
