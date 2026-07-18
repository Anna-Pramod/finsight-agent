"""Tests for numeric provenance (figures traced to retrieved payloads)."""

from app.agents.provenance import (
    extract_monetary_figures,
    supported_universe,
    unverified_figures,
)
from app.agents.response_validator import validate_response
from app.agents.root_agent import AgentTurnResult
from app.mcp.local_transport import LocalDataTransport
from app.schemas.audit import ToolCall
from app.schemas.chat import GroundedAnswer


def test_extract_only_monetary_figures() -> None:
    text = "Net worth is ₹11.36L, or ₹11,35,627. XIRR was 11.5% across 9 funds; ₹1.2Cr target."
    vals = extract_monetary_figures(text)
    assert 1_136_000 in vals          # ₹11.36L
    assert 1_135_627 in vals          # ₹11,35,627
    assert 1.2e7 in vals              # ₹1.2Cr
    assert 11.5 not in vals           # percentage ignored
    assert 9 not in vals              # bare count ignored


def test_universe_includes_leaves_and_sums() -> None:
    payloads = [{"a": {"units": "100000"}, "b": {"units": "250000"}}]
    uni = supported_universe(payloads)
    assert 100_000 in uni and 250_000 in uni
    assert 350_000 in uni  # pairwise sum → aggregate claims verify


def test_rounded_aggregate_verifies() -> None:
    payloads = [{"total": {"units": "1135627"}}]
    # Model rounds to 11.36L; within tolerance → not flagged.
    assert unverified_figures("Your net worth is ₹11.36L.", payloads) == []


def test_fabricated_figure_flagged() -> None:
    payloads = [{"total": {"units": "1135627"}}]
    bad = unverified_figures("You secretly have ₹99,99,999 stashed away.", payloads)
    assert bad == [9_999_999]


def _result(obs: str, tools: int = 1) -> AgentTurnResult:
    return AgentTurnResult(
        answer=GroundedAnswer(observation=obs),
        tools_called=[ToolCall(tool="fetch_net_worth") for _ in range(tools)],
    )


def test_validate_response_blocks_majority_fabrication() -> None:
    payloads = [{"total": {"units": "1135627"}}]
    r = _result("You have ₹50,00,000 in stocks and ₹80,00,000 in gold that we found.")
    verdict = validate_response(r, tool_payloads=payloads)
    assert verdict.blocked and verdict.reason == "unverified_figures"
    assert verdict.unverified_figures


def test_validate_response_passes_grounded_real_payload() -> None:
    payload = LocalDataTransport("8888888888").call_tool("fetch_net_worth", {})
    r = _result(
        "Your total net worth is ₹11,35,627 — mutual funds ₹7,60,627, EPF ₹2,25,000, "
        "and savings ₹1,50,000."
    )
    verdict = validate_response(r, tool_payloads=[payload])
    assert not verdict.blocked
    assert verdict.unverified_figures == []


def test_provenance_skipped_without_payloads() -> None:
    r = _result("Your net worth is ₹11,35,627.")
    assert not validate_response(r, tool_payloads=None).blocked
