"""
Validation loop — parse LLM output as JSON, validate each question via Pydantic.
Rejects any output that doesn't meet the spec.
"""
from __future__ import annotations

import json
import re
import logging
from pydantic import ValidationError
from app.quiz.models import QuizQuestion

logger = logging.getLogger(__name__)


def _strip_markdown_fences(raw: str) -> str:
    """Remove ```json ... ``` wrappers that some LLMs add despite being told not to."""
    stripped = raw.strip()
    # Remove ```json or ``` prefix
    stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
    # Remove ``` suffix
    stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def validate_quiz_output(raw_text: str, expected_count: int) -> list[QuizQuestion]:
    """
    Parse raw LLM text → JSON → list[QuizQuestion].
    Raises ValueError on any failure.
    """
    cleaned = _strip_markdown_fences(raw_text)

    # --- Parse JSON ---
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM output is not valid JSON: {exc}") from exc

    # Must be a list
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array, got {type(data).__name__}.")

    # Count check
    if len(data) != expected_count:
        raise ValueError(f"Expected {expected_count} questions, got {len(data)}.")

    # --- Validate each question via Pydantic ---
    questions: list[QuizQuestion] = []
    errors: list[str] = []
    for i, item in enumerate(data):
        try:
            q = QuizQuestion.model_validate(item)
            questions.append(q)
        except ValidationError as exc:
            errors.append(f"Question {i}: {exc}")

    if errors:
        raise ValueError("Pydantic validation failed:\n" + "\n".join(errors))

    return questions
