"""Risk scoring.

Derives simple, evidence-based debt/risk signals from liabilities, credit
score, and net worth. Deliberately transparent arithmetic (no ML): every
signal cites the numbers it came from.

Implemented in Issue #14.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RiskSignal:
    name: str
    level: str  # "low" | "medium" | "high"
    evidence: str


@dataclass
class RiskAssessment:
    signals: list[RiskSignal] = field(default_factory=list)

    @property
    def overall(self) -> str:
        levels = [s.level for s in self.signals]
        if "high" in levels:
            return "high"
        if "medium" in levels:
            return "medium"
        return "low"


def assess(
    total_assets: float,
    total_liabilities: float,
    credit_score: int | None = None,
) -> RiskAssessment:
    signals: list[RiskSignal] = []

    if total_assets > 0:
        ratio = total_liabilities / total_assets
        level = "low" if ratio < 0.3 else "medium" if ratio < 0.6 else "high"
        signals.append(
            RiskSignal(
                name="leverage",
                level=level,
                evidence=f"liabilities/assets = {ratio:.2f} "
                f"({total_liabilities:,.0f} / {total_assets:,.0f})",
            )
        )
    elif total_liabilities > 0:
        signals.append(
            RiskSignal(
                name="leverage",
                level="high",
                evidence=f"liabilities {total_liabilities:,.0f} with no recorded assets",
            )
        )

    if credit_score is not None:
        level = "low" if credit_score >= 750 else "medium" if credit_score >= 650 else "high"
        signals.append(
            RiskSignal(name="credit_score", level=level, evidence=f"score = {credit_score}")
        )
    else:
        signals.append(
            RiskSignal(
                name="credit_score",
                level="medium",
                evidence="credit score not connected; risk cannot be fully assessed",
            )
        )

    return RiskAssessment(signals=signals)


__all__ = ["RiskSignal", "RiskAssessment", "assess"]
