"""False-positive test for the injection pre-filter.

An over-cautious guardrail is also a failure: if the deterministic pre-filter
blocks ordinary finance questions, the product is broken for real users. This
suite asserts a 0% false-positive rate over ~50 benign queries — several of which
deliberately contain words the filter watches for ("rules", "ignore", "guarantee",
"advisor") in innocent contexts, to prove the filter keys on intent, not keywords.

Runs fully offline (deterministic regex, no model, no backend) so it belongs in CI.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.agents.response_validator import validate_question

BENIGN = Path(__file__).resolve().parents[2] / "evals" / "benign_queries.jsonl"


def _load() -> list[dict]:
    return [json.loads(x) for x in BENIGN.read_text().splitlines() if x.strip()]


def test_benign_queries_dataset_present() -> None:
    cases = _load()
    assert len(cases) >= 50


def test_zero_false_positives() -> None:
    cases = _load()
    blocked = [c["id"] for c in cases if validate_question(c["query"]) is not None]
    # 0% false-positive rate: no benign finance question is pre-filter-blocked.
    assert blocked == [], f"pre-filter false-positives on benign queries: {blocked}"
