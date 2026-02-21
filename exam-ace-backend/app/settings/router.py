"""
Settings API router.
- GET  /settings  — return current user settings (or defaults)
- PUT  /settings  — validate and persist
"""
from __future__ import annotations

import json
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.core.database import get_pool
from app.settings.models import UserSettings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("", response_model=UserSettings)
async def get_settings(user_id: str = Depends(get_current_user)):
    pool = get_pool()
    row = await pool.fetchrow(
        "SELECT * FROM user_settings WHERE user_id = $1::uuid",
        uuid.UUID(user_id),
    )
    if not row:
        # Return defaults (not yet persisted)
        return UserSettings()

    return UserSettings(
        subject=row["subject"],
        difficulty=row["difficulty"],
        question_count=row["question_count"],
        time_limit=row["time_limit"],
        auto_submit=row["auto_submit"],
        show_explanations=row["show_explanations"],
    )


@router.put("", response_model=UserSettings)
async def update_settings(
    body: UserSettings,
    user_id: str = Depends(get_current_user),
):
    pool = get_pool()
    # Upsert
    await pool.execute(
        """
        INSERT INTO user_settings (user_id, subject, difficulty, question_count, time_limit, auto_submit, show_explanations)
        VALUES ($1::uuid, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (user_id) DO UPDATE SET
            subject = EXCLUDED.subject,
            difficulty = EXCLUDED.difficulty,
            question_count = EXCLUDED.question_count,
            time_limit = EXCLUDED.time_limit,
            auto_submit = EXCLUDED.auto_submit,
            show_explanations = EXCLUDED.show_explanations
        """,
        uuid.UUID(user_id),
        body.subject,
        body.difficulty.value,
        body.question_count,
        body.time_limit,
        body.auto_submit,
        body.show_explanations,
    )
    return body
