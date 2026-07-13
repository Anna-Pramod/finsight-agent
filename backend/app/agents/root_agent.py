"""ADK root finance agent.

Builds the root ADK ``LlmAgent`` over the six Fi MCP tools and runs one chat
turn. Specialisation (Net Worth, Loan Affordability, SIP, Debt Risk, Anomaly)
is applied by routing the question to a focus block appended to the shared
instruction (see ``instructions.py``); safety & grounding rules are part of
every instruction and enforced again post-hoc by ``response_validator``.

The agent is wired to a ``FiMcpClient`` whose transport is injected — the live
HTTP transport against a running fi-mcp-dev server, or the local dummy-data
transport — so the agent layer itself is host-agnostic.

Implemented in Issue #6 (specialists folded in via routing, #11-#14).
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types as genai_types

from app.agents.instructions import build_instruction, route_focus
from app.config import get_settings
from app.mcp.fi_client import FiMcpClient
from app.schemas.audit import ToolCall
from app.schemas.chat import GroundedAnswer


@dataclass
class AgentTurnResult:
    """Everything one agent turn produced, pre-validation."""

    answer: GroundedAnswer
    missing_data: list[str] = field(default_factory=list)
    tools_called: list[ToolCall] = field(default_factory=list)
    focus: str = "general"
    raw_text: str = ""


def _make_tools(client: FiMcpClient) -> list[Any]:
    """Six zero-arg functions closing over the client; ADK derives schemas."""

    def fetch_net_worth() -> dict:
        """Fetch the user's net worth: asset values, liabilities, total."""
        return client.fetch_net_worth()

    def fetch_credit_report() -> dict:
        """Fetch the user's credit report: score, loans, account history."""
        return client.fetch_credit_report()

    def fetch_epf_details() -> dict:
        """Fetch the user's EPF (provident fund) account details."""
        return client.fetch_epf_details()

    def fetch_mf_transactions() -> dict:
        """Fetch the user's mutual fund transactions (SIPs, lump sums)."""
        return client.fetch_mf_transactions()

    def fetch_bank_transactions() -> dict:
        """Fetch the user's bank transactions."""
        return client.fetch_bank_transactions()

    def fetch_stock_transactions() -> dict:
        """Fetch the user's Indian and US stock transactions."""
        return client.fetch_stock_transactions()

    return [
        fetch_net_worth,
        fetch_credit_report,
        fetch_epf_details,
        fetch_mf_transactions,
        fetch_bank_transactions,
        fetch_stock_transactions,
    ]


def _is_retryable(exc: BaseException, depth: int = 0) -> bool:
    """True for rate-limit/availability errors anywhere in the exception tree.

    Walks __cause__/__context__ chains and ExceptionGroup members; matches by
    message because ADK wraps genai errors in private exception classes.
    """
    if depth > 8 or exc is None:
        return False
    text = f"{type(exc).__name__}: {exc}".lower()
    if any(m in text for m in ("resource_exhausted", "unavailable", "429", "503")):
        return True
    if isinstance(exc, BaseExceptionGroup):
        if any(_is_retryable(e, depth + 1) for e in exc.exceptions):
            return True
    for linked in (exc.__cause__, exc.__context__):
        if linked is not None and _is_retryable(linked, depth + 1):
            return True
    return False


def _parse_answer(text: str) -> tuple[GroundedAnswer, list[str]]:
    """Parse the model's JSON reply into a GroundedAnswer + missing-data list."""
    cleaned = text.strip()
    # Tolerate accidental markdown fences despite the instruction.
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to treating the whole reply as the observation.
        return GroundedAnswer(observation=cleaned), []
    answer = GroundedAnswer(
        observation=str(data.get("observation", "")).strip() or cleaned,
        risk=data.get("risk") or None,
        suggested_next_step=data.get("suggested_next_step") or None,
        assumptions=[str(a) for a in data.get("assumptions", []) if a],
    )
    missing = [str(m) for m in data.get("missing_data", []) if m]
    return answer, missing


async def run_agent_turn(question: str, client: FiMcpClient, trace_recorder: Any) -> AgentTurnResult:
    """Run one question through the ADK agent and return the structured result.

    ``trace_recorder`` is the ToolTraceRecorder already wrapped inside the
    client's transport; its calls list is read back after the run.
    """
    settings = get_settings()
    # ADK/genai reads credentials from the process env, not our Settings.
    if settings.google_api_key and not os.environ.get("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
    focus = route_focus(question)

    agent = LlmAgent(
        name="finsight_root",
        model=settings.gemini_model,
        instruction=build_instruction(question),
        tools=_make_tools(client),
    )

    runner = InMemoryRunner(agent=agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="demo"
    )

    final_text = ""
    # Gemini free tier: transient 503s under load and 429s at 5 req/min.
    # Retry with a backoff long enough to clear the per-minute window.
    delays = (5.0, 20.0, 35.0)
    for attempt in range(len(delays) + 1):
        try:
            async for event in runner.run_async(
                user_id="demo",
                session_id=session.id,
                new_message=genai_types.Content(
                    role="user", parts=[genai_types.Part(text=question)]
                ),
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_text = "".join(p.text or "" for p in event.content.parts)
            break
        except Exception as exc:
            if attempt == len(delays) or not _is_retryable(exc):
                raise
            await asyncio.sleep(delays[attempt])

    answer, missing = _parse_answer(final_text)
    return AgentTurnResult(
        answer=answer,
        missing_data=missing,
        tools_called=list(trace_recorder.calls),
        focus=focus,
        raw_text=final_text,
    )


__all__ = ["AgentTurnResult", "run_agent_turn"]
