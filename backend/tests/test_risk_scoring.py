"""Tests for risk scoring (Issue #14)."""

from app.services.risk_scoring import assess


def test_low_leverage_good_score_is_low() -> None:
    a = assess(total_assets=1_000_000, total_liabilities=100_000, credit_score=790)
    assert a.overall == "low"


def test_high_leverage_dominates() -> None:
    a = assess(total_assets=1_000_000, total_liabilities=800_000, credit_score=790)
    assert a.overall == "high"
    leverage = next(s for s in a.signals if s.name == "leverage")
    assert "0.80" in leverage.evidence


def test_missing_credit_score_is_disclosed_medium() -> None:
    a = assess(total_assets=1_000_000, total_liabilities=100_000, credit_score=None)
    score = next(s for s in a.signals if s.name == "credit_score")
    assert score.level == "medium" and "not connected" in score.evidence
