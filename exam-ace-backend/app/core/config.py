"""
Application configuration — reads .env and crashes hard if required vars are missing.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # --- Supabase ---
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_jwt_secret: str = Field(..., description="Supabase JWT secret for token verification")

    # --- Database ---
    database_url: str = Field(..., description="Postgres connection string (asyncpg format)")

    # --- Redis ---
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")

    # --- LLM ---
    llm_provider: str = Field(default="local", description="openai | mistral | local")
    llm_api_key: str = Field(default="not-needed", description="API key (not needed for local)")
    llm_base_url: str = Field(default="http://localhost:1234/v1", description="LM Studio default endpoint")
    llm_model: str = Field(default="phi-3-mini-4k-instruct", description="Model name as shown in LM Studio")
    llm_health_timeout: int = Field(default=3, description="Seconds to wait when checking model connectivity")

    # --- App ---
    cors_origins: str = Field(default="http://localhost:5173", description="Comma-separated CORS origins")

    # --- Rate Limiting ---
    quiz_rate_limit: int = Field(default=20, description="Max quiz generations per hour per user")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton — import this everywhere
settings = Settings()
