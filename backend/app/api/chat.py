"""Chat endpoint (POST /chat).

Accepts a user question + persona, runs the ADK agent over the persona's data,
validates the answer for safety/grounding, records the audit trail, and returns
a grounded answer with the tool trace.

Transport selection (settings.fi_mcp_mode):
- ``local`` (default): in-process dummy-data transport over the upstream
  ``test_data_dir`` files — no Go server needed; what the hosted demo uses.
- ``http``: the live fi-mcp-dev server via the shared ``mcp-session-…`` id.

Implemented in Issue #9.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.agents.response_validator import validate_question, validate_response
from app.agents.root_agent import _is_retryable as _is_model_unavailable
from app.agents.root_agent import run_agent_turn
from app.agents.session_manager import SessionManager
from app.config import get_settings
from app.mcp.fi_client import FiMcpClient, HttpStreamTransport, LoginRequired
from app.mcp.local_transport import LocalDataTransport, PersonaDataNotFound
from app.mcp.persona_mapping import resolve_phone
from app.mcp.tool_trace import ToolTraceRecorder
from app.schemas.audit import AuditRecord
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.audit_logger import audit_log

router = APIRouter(tags=["chat"])

# Process-wide session manager (in-memory, like the upstream server's sessions).
session_manager = SessionManager()


def _build_transport(phone: str, session_id: str) -> object:
    settings = get_settings()
    if settings.fi_mcp_mode == "http":
        return HttpStreamTransport(settings.mcp_stream_url, session_id)
    try:
        return LocalDataTransport(phone)
    except PersonaDataNotFound as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    try:
        phone = resolve_phone(req.persona)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown persona: {req.persona}")

    session = session_manager.get_or_create(req.persona, phone, req.session_id)

    # Pre-flight: block prompt-injection before any model or tool runs.
    pre = validate_question(req.question)
    if pre is not None:
        response = ChatResponse(
            session_id=session.session_id,
            persona=req.persona,
            answer=pre.answer,
            blocked=True,
        )
        _audit(session.session_id, req, response)
        return response

    trace = ToolTraceRecorder(inner=_build_transport(phone, session.session_id))
    client = FiMcpClient(trace)

    try:
        result = await run_agent_turn(req.question, client, trace)
    except LoginRequired as exc:
        raise HTTPException(
            status_code=409,
            detail={"status": "login_required", "login_url": exc.login_url},
        )
    except Exception as exc:  # surface model quota/availability cleanly, not as a 500
        if _is_model_unavailable(exc):
            raise HTTPException(
                status_code=503,
                detail="The reasoning model is temporarily unavailable (rate limit or high demand). Please try again shortly.",
            )
        raise

    verdict = validate_response(result, tool_payloads=trace.payloads)
    response = ChatResponse(
        session_id=session.session_id,
        persona=req.persona,
        answer=verdict.answer,
        tools_called=result.tools_called,
        missing_data=result.missing_data,
        blocked=verdict.blocked,
    )
    _audit(session.session_id, req, response)
    return response


def _audit(session_id: str, req: ChatRequest, resp: ChatResponse) -> None:
    audit_log.record(
        AuditRecord(
            session_id=session_id,
            persona=req.persona,
            question=req.question,
            tools_called=resp.tools_called,
            missing_data=resp.missing_data,
            blocked=resp.blocked,
        )
    )


__all__ = ["router"]
