"""
Prompt templates for quiz generation.
Temperature mapping per difficulty level.
"""
from __future__ import annotations

from app.quiz.models import Difficulty

# Temperature mapping — harder questions get lower temperature for precision
TEMPERATURE_MAP: dict[Difficulty, float] = {
    Difficulty.beginner: 0.7,
    Difficulty.intermediate: 0.5,
    Difficulty.advanced: 0.3,
}

SYSTEM_PROMPT = (
    "You are an exam question generator. "
    "You produce high-quality, exam-level multiple choice questions. "
    "You ALWAYS respond with valid JSON only — no prose, no markdown, no code fences."
)


def build_user_prompt(subject: str, difficulty: Difficulty, count: int) -> str:
    return (
        f"Generate EXACTLY {count} multiple choice questions.\n\n"
        f"Subject: {subject}\n"
        f"Difficulty: {difficulty.value}\n\n"
        "Rules:\n"
        "- Each question must be exam-level\n"
        "- 4 options only\n"
        "- 1 correct answer\n"
        "- Include a concise explanation for the correct answer\n"
        "- Return VALID JSON ONLY\n\n"
        "Return a JSON array where each element has this shape:\n"
        '{"question": "...", "options": ["A","B","C","D"], "correct_index": 0, "explanation": "..."}\n\n'
        "No prose. No markdown. JSON array only."
    )
