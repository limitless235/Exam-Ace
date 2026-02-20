"""
FastAPI dependency to extract the current user from request.state.
"""
from __future__ import annotations

from fastapi import Request, HTTPException, status


def get_current_user(request: Request) -> str:
    """Return the authenticated user_id.  Raises 401 if missing."""
    user_id: str | None = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")
    return user_id
