"""
Redis-backed sliding-window rate limiter.
Default: 20 quiz generations per hour per user.  Returns 429 on breach.
"""
from __future__ import annotations

import time
import logging
from fastapi import HTTPException, status

from app.core import redis as redis_mod

logger = logging.getLogger(__name__)


async def check_rate_limit(user_id: str, limit: int, window_seconds: int = 3600) -> None:
    """
    Raise 429 if the user has exceeded `limit` requests in the rolling `window_seconds`.
    If Redis is unavailable, silently allow the request (graceful degradation).
    """
    client = redis_mod.get_redis()
    if client is None:
        return  # Redis down → skip limiting

    key = f"rate:quiz:{user_id}"
    now = time.time()
    window_start = now - window_seconds

    pipe = client.pipeline()
    # Remove entries older than the window
    pipe.zremrangebyscore(key, 0, window_start)
    # Count remaining entries
    pipe.zcard(key)
    # Add current request
    pipe.zadd(key, {str(now): now})
    # Set expiry on the key so it auto-cleans
    pipe.expire(key, window_seconds)
    results = await pipe.execute()

    current_count = results[1]
    if current_count >= limit:
        logger.warning("Rate limit hit for user %s (%d/%d)", user_id, current_count, limit)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {limit} quiz generations per hour.",
        )
