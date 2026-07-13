"""Audit endpoint (GET /audit/{session_id}).

Returns the audit trail of tool calls and data usage for a demo session — the
backing data for the frontend's tool-trace / transparency panel.

Implemented in Issue #10.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.audit import AuditRecord
from app.services.audit_logger import audit_log

router = APIRouter(tags=["audit"])


@router.get("/audit/{session_id}", response_model=list[AuditRecord])
def audit(session_id: str) -> list[AuditRecord]:
    """Audit records for a session (empty list if none)."""
    return audit_log.for_session(session_id)


__all__ = ["router"]
