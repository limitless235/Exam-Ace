"""
Async PostgreSQL connection pool via asyncpg.
Initialised at app startup, torn down at shutdown.
"""
from __future__ import annotations

import asyncpg
from asyncpg import Pool

_pool: Pool | None = None


async def init_db(dsn: str) -> Pool:
    """Create and return a connection pool."""
    global _pool
    _pool = await asyncpg.create_pool(dsn=dsn, min_size=2, max_size=10)
    return _pool


async def close_db() -> None:
    """Close the connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> Pool:
    """Return the active pool.  Raises if not initialised."""
    if _pool is None:
        raise RuntimeError("Database pool is not initialised. Call init_db() first.")
    return _pool
