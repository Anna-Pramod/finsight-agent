"""Snapshot endpoint (GET /snapshot/{persona}).

Deterministic (no-LLM) summary of a persona's finances for the dashboard:
net worth breakdown from ``fetch_net_worth``, credit score from
``fetch_credit_report``, and evidence-based risk signals from the risk-scoring
service. Uses the same transport layer as chat, so it reflects exactly the
data the agent sees.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.mcp.local_transport import LocalDataTransport, PersonaDataNotFound
from app.mcp.persona_mapping import resolve_phone
from app.services.risk_scoring import assess

router = APIRouter(tags=["snapshot"])


class RiskSignalOut(BaseModel):
    name: str
    level: str
    evidence: str


class SnapshotOut(BaseModel):
    persona: str
    total_net_worth: float
    assets: dict[str, float] = Field(default_factory=dict)
    liabilities: dict[str, float] = Field(default_factory=dict)
    credit_score: int | None = None
    risk_overall: str
    risk_signals: list[RiskSignalOut] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)


def _units(value: dict) -> float:
    try:
        return float(value.get("units", 0) or 0)
    except (TypeError, ValueError):
        return 0.0


@router.get("/snapshot/{persona}", response_model=SnapshotOut)
def snapshot(persona: str) -> SnapshotOut:
    try:
        phone = resolve_phone(persona)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown persona: {persona}")
    try:
        transport = LocalDataTransport(phone)
    except PersonaDataNotFound as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    missing: list[str] = []

    nw = transport.call_tool("fetch_net_worth", {})
    nw_resp = nw.get("netWorthResponse", {})
    assets: dict[str, float] = {}
    liabilities: dict[str, float] = {}
    for item in nw_resp.get("assetValues", []):
        name = item.get("netWorthAttribute", "ASSET").replace("ASSET_TYPE_", "").title().replace("_", " ")
        assets[name] = _units(item.get("value", {}))
    for item in nw_resp.get("liabilityValues", []):
        name = item.get("netWorthAttribute", "LIABILITY").replace("LIABILITY_TYPE_", "").title().replace("_", " ")
        liabilities[name] = _units(item.get("value", {}))
    total = _units(nw_resp.get("totalNetWorthValue", {}))
    if not nw_resp:
        missing.append("net worth")

    credit = transport.call_tool("fetch_credit_report", {})
    score: int | None = None
    reports = credit.get("creditReports") or []
    if reports:
        raw = (
            reports[0]
            .get("creditReportData", {})
            .get("score", {})
            .get("bureauScore")
        )
        try:
            score = int(raw) if raw is not None else None
        except (TypeError, ValueError):
            score = None
    if score is None:
        missing.append("credit score")

    risk = assess(
        total_assets=sum(assets.values()),
        total_liabilities=sum(liabilities.values()),
        credit_score=score,
    )

    return SnapshotOut(
        persona=persona,
        total_net_worth=total,
        assets=assets,
        liabilities=liabilities,
        credit_score=score,
        risk_overall=risk.overall,
        risk_signals=[
            RiskSignalOut(name=s.name, level=s.level, evidence=s.evidence) for s in risk.signals
        ],
        missing_data=missing,
    )


__all__ = ["router"]
