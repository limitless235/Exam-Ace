"""
ExamAce Backend — FastAPI application entry point.

Registers:
  - JWT auth middleware (rejects unauthenticated requests globally)
  - CORS
  - Lifespan events (DB pool, Redis connection)
  - All API routers
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hook — initialise DB pool and Redis."""
    from app.core.config import settings
    from app.core.database import init_db, close_db
    from app.core.redis import init_redis, close_redis

    logger.info("Starting ExamAce backend …")
    await init_db(settings.database_url)
    await init_redis(settings.redis_url)
    logger.info("Database and Redis ready.")
    yield
    await close_db()
    await close_redis()
    logger.info("Shutdown complete.")


def create_app() -> FastAPI:
    from app.core.config import settings

    app = FastAPI(
        title="ExamAce API",
        version="1.0.0",
        description="Real AI-powered exam preparation platform.",
        lifespan=lifespan,
    )

    # --- CORS ---
    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Auth middleware ---
    from app.auth.middleware import JWTAuthMiddleware
    app.add_middleware(JWTAuthMiddleware, jwt_secret=settings.supabase_jwt_secret, supabase_url=settings.supabase_url)

    # --- Routers ---
    from app.quiz.router import router as quiz_router
    from app.settings.router import router as settings_router
    from app.users.router import router as users_router
    from app.analytics.router import router as analytics_router

    app.include_router(quiz_router)
    app.include_router(settings_router)
    app.include_router(users_router)
    app.include_router(analytics_router)

    # --- Health check (public) ---
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "service": "exam-ace-backend"}

    return app


app = create_app()
