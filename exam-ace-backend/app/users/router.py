"""
Users API router.
- GET /users/me — return profile for the authenticated user
"""
from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.core.database import get_pool

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user)):
    pool = get_pool()
    row = await pool.fetchrow(
        "SELECT id, email, display_name, created_at FROM profiles WHERE id = $1::uuid",
        uuid.UUID(user_id),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {
        "id": str(row["id"]),
        "email": row["email"],
        "display_name": row["display_name"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
    }
