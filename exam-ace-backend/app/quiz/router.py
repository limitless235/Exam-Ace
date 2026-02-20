"""
Quiz API router.
- POST /quiz/generate  — validate, call LLM, store, return questions (no answers)
- POST /quiz/submit    — recompute score server-side, detect tampering, save attempt
- GET  /quiz/history   — list past attempts for current user
"""
from __future__ import annotations

import json
import uuid
import hashlib
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.core.database import get_pool
from app.core.rate_limiter import check_rate_limit
from app.quiz.models import (
    Difficulty,
    GenerateRequest,
    GenerateResponse,
    QuizQuestionPublic,
    SubmitRequest,
    SubmitResponse,
    QuestionResult,
    QuizQuestion,
)
from app.quiz.generator import generate_quiz
from app.quiz.llm_gateway import get_provider

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quiz", tags=["Quiz"])


def _get_llm_provider():
    """Build LLM provider from config (deferred import to avoid startup crash during tests)."""
    from app.core.config import settings
    return get_provider(
        settings.llm_provider,
        settings.llm_api_key,
        settings.llm_base_url,
        model=settings.llm_model,
        health_timeout=settings.llm_health_timeout,
    )


# --------------------------------------------------------------------------
# POST /quiz/generate
# --------------------------------------------------------------------------

@router.post("/generate", response_model=GenerateResponse)
async def generate_quiz_endpoint(
    body: GenerateRequest,
    user_id: str = Depends(get_current_user),
):
    # Rate limit
    from app.core.config import settings
    await check_rate_limit(user_id, limit=settings.quiz_rate_limit)

    # Generate via LLM (falls back to question bank if unreachable)
    provider = _get_llm_provider()
    try:
        questions, source = await generate_quiz(provider, body.subject, body.difficulty, body.count)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))

    # Store quiz snapshot in DB
    quiz_id = str(uuid.uuid4())
    pool = get_pool()
    questions_json = json.dumps([q.model_dump() for q in questions])

    await pool.execute(
        """
        INSERT INTO quiz_attempts (id, user_id, subject, difficulty, questions)
        VALUES ($1, $2::uuid, $3, $4, $5::jsonb)
        """,
        uuid.UUID(quiz_id),
        uuid.UUID(user_id),
        body.subject,
        body.difficulty.value,
        questions_json,
    )

    # Return questions WITHOUT correct_index / explanation
    public_questions = [
        QuizQuestionPublic(index=i, question=q.question, options=q.options)
        for i, q in enumerate(questions)
    ]
    return GenerateResponse(
        quiz_id=quiz_id,
        questions=public_questions,
        subject=body.subject,
        difficulty=body.difficulty,
        source=source,
    )


# --------------------------------------------------------------------------
# POST /quiz/submit
# --------------------------------------------------------------------------

@router.post("/submit", response_model=SubmitResponse)
async def submit_quiz_endpoint(
    body: SubmitRequest,
    user_id: str = Depends(get_current_user),
):
    pool = get_pool()

    # Fetch the quiz from DB
    row = await pool.fetchrow(
        "SELECT * FROM quiz_attempts WHERE id = $1 AND user_id = $2::uuid",
        uuid.UUID(body.quiz_id),
        uuid.UUID(user_id),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    # Deserialize stored questions
    stored_questions_raw = row["questions"]
    if isinstance(stored_questions_raw, str):
        stored_questions_raw = json.loads(stored_questions_raw)
    questions = [QuizQuestion.model_validate(q) for q in stored_questions_raw]

    # Anti-cheat: answer count must match question count
    if len(body.answers) != len(questions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Expected {len(questions)} answers, got {len(body.answers)}.",
        )

    # Validate answer indices
    for i, ans in enumerate(body.answers):
        if not (0 <= ans <= 3):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Answer index {ans} for question {i} is out of range [0, 3].",
            )

    # Server-side score recomputation
    correct = sum(1 for q, a in zip(questions, body.answers) if q.correct_index == a)
    total = len(questions)
    score = round((correct / total) * 100, 2)

    # Build detailed results
    results = [
        QuestionResult(
            question=q.question,
            options=q.options,
            selected_index=a,
            correct_index=q.correct_index,
            is_correct=(q.correct_index == a),
            explanation=q.explanation,
        )
        for q, a in zip(questions, body.answers)
    ]

    # Update DB with answers and score
    answers_json = json.dumps(body.answers)
    await pool.execute(
        """
        UPDATE quiz_attempts
        SET answers = $1::jsonb, score = $2
        WHERE id = $3 AND user_id = $4::uuid
        """,
        answers_json,
        score,
        uuid.UUID(body.quiz_id),
        uuid.UUID(user_id),
    )

    return SubmitResponse(
        quiz_id=body.quiz_id,
        score=score,
        total=total,
        correct=correct,
        results=results,
    )


# --------------------------------------------------------------------------
# GET /quiz/history
# --------------------------------------------------------------------------

@router.get("/history")
async def quiz_history(user_id: str = Depends(get_current_user)):
    pool = get_pool()
    rows = await pool.fetch(
        """
        SELECT id, subject, difficulty, score, created_at
        FROM quiz_attempts
        WHERE user_id = $1::uuid
        ORDER BY created_at DESC
        LIMIT 50
        """,
        uuid.UUID(user_id),
    )
    return [
        {
            "id": str(row["id"]),
            "subject": row["subject"],
            "difficulty": row["difficulty"],
            "score": row["score"],
            "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        }
        for row in rows
    ]


# --------------------------------------------------------------------------
# POST /quiz/record — persist a locally-scored quiz attempt
# --------------------------------------------------------------------------

from pydantic import BaseModel, Field as PydanticField

class RecordAttemptRequest(BaseModel):
    subject: str
    difficulty: str
    score: float = PydanticField(..., ge=0, le=100)
    total: int = PydanticField(..., ge=1)
    correct: int = PydanticField(..., ge=0)


@router.post("/record")
async def record_quiz_attempt(
    body: RecordAttemptRequest,
    user_id: str = Depends(get_current_user),
):
    pool = get_pool()
    attempt_id = uuid.uuid4()

    await pool.execute(
        """
        INSERT INTO quiz_attempts (id, user_id, subject, difficulty, questions, score)
        VALUES ($1, $2::uuid, $3, $4, $5::jsonb, $6)
        """,
        attempt_id,
        uuid.UUID(user_id),
        body.subject,
        body.difficulty,
        json.dumps([]),  # no question data for local quizzes
        body.score,
    )

    logger.info("Recorded local quiz attempt %s for user %s: %s/%s (%s%%)",
                attempt_id, user_id, body.correct, body.total, body.score)

    return {"status": "recorded", "id": str(attempt_id)}

