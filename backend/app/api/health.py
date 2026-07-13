"""Health endpoint (GET /health).

Liveness/readiness check returning service status, version, and environment.

Implemented in Issue #4.
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import get_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str
    env: str


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return service liveness information."""
    settings = get_settings()
    return HealthResponse(status="ok", version="0.0.1", env=settings.app_env)


__all__ = ["router", "HealthResponse"]
