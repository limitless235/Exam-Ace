"""
Domain models — single source of truth for the entire application.
Frontend, backend, and DB must use these exact enum strings and model shapes.
"""
from __future__ import annotations

import uuid
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Difficulty(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


# ---------------------------------------------------------------------------
# Quiz question (canonical shape returned by LLM and stored in DB)
# ---------------------------------------------------------------------------

class QuizQuestion(BaseModel):
    question: str = Field(..., min_length=1)
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_index: int = Field(..., ge=0, le=3)
    explanation: str = Field(..., min_length=1)

    @field_validator("options")
    @classmethod
    def options_must_have_four(cls, v: list[str]) -> list[str]:
        if len(v) != 4:
            raise ValueError("Each question must have exactly 4 options.")
        return v


# ---------------------------------------------------------------------------
# API request / response models
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    difficulty: Difficulty
    count: int = Field(default=10, ge=3, le=30)


class QuizQuestionPublic(BaseModel):
    """Sent to the frontend — no correct_index or explanation."""
    index: int
    question: str
    options: list[str]


class GenerateResponse(BaseModel):
    quiz_id: str
    questions: list[QuizQuestionPublic]
    subject: str
    difficulty: Difficulty
    source: str = Field(default="ai", description="'ai' or 'practice_bank'")


class SubmitRequest(BaseModel):
    quiz_id: str
    answers: list[int]  # selected option index per question


class QuestionResult(BaseModel):
    question: str
    options: list[str]
    selected_index: int
    correct_index: int
    is_correct: bool
    explanation: str


class SubmitResponse(BaseModel):
    quiz_id: str
    score: float
    total: int
    correct: int
    results: list[QuestionResult]


# ---------------------------------------------------------------------------
# Quiz attempt (DB record shape)
# ---------------------------------------------------------------------------

class QuizAttempt(BaseModel):
    id: str
    user_id: str
    subject: str
    difficulty: Difficulty
    questions: list[QuizQuestion]
    answers: list[int] | None = None
    score: float | None = None
    created_at: datetime | None = None
