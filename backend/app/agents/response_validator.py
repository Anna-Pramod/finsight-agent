"""Response safety/grounding validator.

Post-processes agent output before it reaches the user:

- blocks prompt-injection attempts (both in the question and echoed in output);
- blocks regulated-advice phrasing (guarantees, buy/sell instructions);
- requires that answers which quote figures actually ran tools (grounding);
- the disclaimer travels on every ChatResponse via its schema default.

This is a deterministic guardrail layered on top of the instruction-level
rules — defence in depth, and independently testable. Implemented in Issue #7.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.agents.root_agent import AgentTurnResult
from app.schemas.chat import GroundedAnswer

# Patterns that indicate the *question* is trying to subvert the agent.
INJECTION_PATTERNS = [
    r"ignore (all |any |your |previous |prior )*(instructions|rules|guidelines)",
    r"disregard (all |any |your |previous |prior )*(instructions|rules|safety)",
    r"(reveal|show|print|repeat) (me )?(your|the) (system )?(prompt|instructions)",
    r"you are no longer",
    r"pretend (you are|to be)",
    r"act as (if|though|a different)",
    r"jailbreak",
    r"developer mode",
    r"fabricate|make up (the |some )?(data|numbers|figures)",
    r"guarantee (me )?(a |the )?loan",
]

# Output phrasing that would cross the not-an-advisor line.
FORBIDDEN_OUTPUT_PATTERNS = [
    r"\bguaranteed? (approval|returns?|profit)",
    r"\byou (will|are certain to) (be approved|get the loan|profit)",
    r"\b(buy|sell|dump|short) (this|that|the|your) (stock|fund|share)",
    r"\byou should (buy|sell) \b",
    r"\bI (guarantee|promise)\b",
]

REFUSAL = GroundedAnswer(
    observation=(
        "I can't help with that request. It appears to ask me to ignore my "
        "safety and grounding rules (e.g. fabricate data, reveal instructions, "
        "or give guaranteed/regulated advice), which I won't do. I'm happy to "
        "answer questions grounded in your connected financial data."
    ),
    risk=None,
    suggested_next_step="Ask a question about your net worth, loans, SIPs, EPF, or transactions.",
)


@dataclass
class ValidationResult:
    answer: GroundedAnswer
    blocked: bool
    reason: str | None = None


def is_injection(question: str) -> bool:
    q = question.lower()
    return any(re.search(p, q) for p in INJECTION_PATTERNS)


def validate_question(question: str) -> ValidationResult | None:
    """Pre-flight check. Returns a blocking result for injection attempts."""
    if is_injection(question):
        return ValidationResult(answer=REFUSAL, blocked=True, reason="prompt_injection")
    return None


def validate_response(result: AgentTurnResult) -> ValidationResult:
    """Post-hoc check of the agent's structured answer."""
    text = " ".join(
        filter(
            None,
            [
                result.answer.observation,
                result.answer.risk or "",
                result.answer.suggested_next_step or "",
            ],
        )
    ).lower()

    for pattern in FORBIDDEN_OUTPUT_PATTERNS:
        if re.search(pattern, text):
            return ValidationResult(
                answer=REFUSAL, blocked=True, reason=f"forbidden_output:{pattern}"
            )

    # Grounding: an answer quoting rupee figures must have called at least one tool.
    quotes_figures = bool(re.search(r"(₹|\binr\b|\brs\.?\s?\d)", text))
    if quotes_figures and not result.tools_called:
        return ValidationResult(
            answer=GroundedAnswer(
                observation=(
                    "I couldn't ground an answer in your connected data for this "
                    "question (no data tools were used), so I won't quote figures."
                ),
                suggested_next_step="Try rephrasing the question about your connected accounts.",
            ),
            blocked=True,
            reason="ungrounded_figures",
        )

    return ValidationResult(answer=result.answer, blocked=False)


__all__ = [
    "ValidationResult",
    "validate_question",
    "validate_response",
    "is_injection",
    "REFUSAL",
]
