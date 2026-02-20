"""
User settings Pydantic model — mirrors the user_settings DB table exactly.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.quiz.models import Difficulty


class UserSettings(BaseModel):
    subject: str = Field(default="General Knowledge", min_length=1, max_length=200)
    difficulty: Difficulty = Field(default=Difficulty.beginner)
    question_count: int = Field(default=10, ge=3, le=30)
    time_limit: int | None = Field(default=None, ge=1, le=120, description="Minutes, null = no limit")
    auto_submit: bool = Field(default=False)
    show_explanations: bool = Field(default=True)
