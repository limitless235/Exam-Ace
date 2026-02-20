"""
Quiz generator orchestrator.
Flow: check health → call LLM → validate → retry → fallback if all else fails.
Returns (questions, source) where source is "ai" or "practice_bank".
"""
from __future__ import annotations

import logging
from app.quiz.models import Difficulty, QuizQuestion
from app.quiz.prompts import SYSTEM_PROMPT, build_user_prompt, TEMPERATURE_MAP
from app.quiz.llm_gateway import LLMProvider
from app.quiz.validator import validate_quiz_output
from app.quiz.fallback_questions import get_fallback_questions

logger = logging.getLogger(__name__)

_MAX_ATTEMPTS = 3  # initial + 2 retries


async def generate_quiz(
    provider: LLMProvider,
    subject: str,
    difficulty: Difficulty,
    count: int,
) -> tuple[list[QuizQuestion], str]:
    """
    Generate `count` validated quiz questions.

    1. Check if the LLM endpoint is reachable.
    2. If reachable, call LLM with retry loop.
    3. If unreachable OR all retries fail, fall back to the curated question bank.

    Returns:
        (questions, source) — source is "ai" or "practice_bank"
    """

    # --- Health check ---
    is_healthy = await provider.check_health()
    if not is_healthy:
        logger.warning("LLM provider is unreachable — using fallback question bank.")
        return get_fallback_questions(subject, difficulty, count), "practice_bank"

    # --- LLM generation with retries ---
    temperature = TEMPERATURE_MAP[difficulty]
    user_prompt = build_user_prompt(subject, difficulty, count)
    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            logger.info("LLM attempt %d/%d for %s/%s/%d", attempt, _MAX_ATTEMPTS, subject, difficulty.value, count)
            raw_output = await provider.generate(SYSTEM_PROMPT, user_prompt, temperature)
            questions = validate_quiz_output(raw_output, count)
            logger.info("LLM attempt %d succeeded — %d valid questions.", attempt, len(questions))
            return questions, "ai"
        except (ValueError, Exception) as exc:
            last_error = exc
            logger.warning("LLM attempt %d failed: %s", attempt, exc)

    # --- All LLM attempts exhausted — fall back ---
    logger.error(
        "Quiz generation failed after %d attempts (last error: %s). Falling back to question bank.",
        _MAX_ATTEMPTS, last_error,
    )
    return get_fallback_questions(subject, difficulty, count), "practice_bank"
