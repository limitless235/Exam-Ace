"""
Analytics API router.
- GET /analytics/performance — aggregated quiz performance for current user
"""
from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.core.database import get_pool

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/performance")
async def get_performance(user_id: str = Depends(get_current_user)):
    pool = get_pool()

    # Overall stats
    overall = await pool.fetchrow(
        """
        SELECT
            COUNT(*)::int AS total_quizzes,
            COALESCE(AVG(score), 0) AS avg_score,
            COALESCE(MAX(score), 0) AS best_score,
            COALESCE(MIN(score), 0) AS worst_score
        FROM quiz_attempts
        WHERE user_id = $1::uuid AND score IS NOT NULL
        """,
        uuid.UUID(user_id),
    )

    # Per-subject breakdown
    by_subject = await pool.fetch(
        """
        SELECT
            subject,
            COUNT(*)::int AS attempts,
            ROUND(AVG(score)::numeric, 2) AS avg_score
        FROM quiz_attempts
        WHERE user_id = $1::uuid AND score IS NOT NULL
        GROUP BY subject
        ORDER BY attempts DESC
        """,
        uuid.UUID(user_id),
    )

    # Per-difficulty breakdown
    by_difficulty = await pool.fetch(
        """
        SELECT
            difficulty,
            COUNT(*)::int AS attempts,
            ROUND(AVG(score)::numeric, 2) AS avg_score
        FROM quiz_attempts
        WHERE user_id = $1::uuid AND score IS NOT NULL
        GROUP BY difficulty
        ORDER BY difficulty
        """,
        uuid.UUID(user_id),
    )

    # Recent trend (last 10 quizzes)
    recent = await pool.fetch(
        """
        SELECT subject, difficulty, score, created_at
        FROM quiz_attempts
        WHERE user_id = $1::uuid AND score IS NOT NULL
        ORDER BY created_at DESC
        LIMIT 10
        """,
        uuid.UUID(user_id),
    )

    return {
        "overall": {
            "total_quizzes": overall["total_quizzes"],
            "avg_score": float(overall["avg_score"]),
            "best_score": float(overall["best_score"]),
            "worst_score": float(overall["worst_score"]),
        },
        "by_subject": [
            {"subject": r["subject"], "attempts": r["attempts"], "avg_score": float(r["avg_score"])}
            for r in by_subject
        ],
        "by_difficulty": [
            {"difficulty": r["difficulty"], "attempts": r["attempts"], "avg_score": float(r["avg_score"])}
            for r in by_difficulty
        ],
        "recent": [
            {
                "subject": r["subject"],
                "difficulty": r["difficulty"],
                "score": r["score"],
                "created_at": r["created_at"].isoformat() if r["created_at"] else None,
            }
            for r in recent
        ],
    }
