"""FinSight Agent — FastAPI application entrypoint.

Creates the FastAPI app, configures CORS from settings, and mounts the API
routers. Chat/personas/audit routers are added as their issues land; the health
router and CORS are wired here (Issues #3, #4).
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import audit, chat, health, personas, snapshot
from app.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="FinSight Agent API",
        version="0.0.1",
        description="Agentic fintech assistant over Fi MCP Dev (Google ADK + Gemini).",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(personas.router)
    app.include_router(audit.router)
    app.include_router(snapshot.router)

    return app


app = create_app()

__all__ = ["app", "create_app"]
