# Evaluation

How FinSight's quality, grounding, and safety are measured. Everything here is in
[`evals/`](../evals/) and reproducible with `python evals/run_evals.py`.

## Datasets

| File | What it is |
|------|-----------|
| `test_queries.jsonl` | Realistic workflow questions (net worth, loan, SIP, risk, missing-data) with the persona to run each against. |
| `expected_tool_calls.jsonl` | Per-query expectations: which `fetch_*` tools must run, whether assumptions/missing-data must be disclosed, and forbidden outcomes (`must_not`). |
| `prompt_injection_tests.jsonl` | 12 adversarial attacks across 9 classes, each labelled with its `attack_class`. |
| `benign_queries.jsonl` | 50 ordinary finance questions — the false-positive control set. |

## What's scored

- **Tool-call correctness** — the expected tools were called.
- **Grounding & provenance** — no fabricated figures; monetary figures trace to the
  retrieved payload (enforced at runtime by the validator, see [`safety.md`](safety.md)).
- **Missing-data disclosure** — gaps (no benchmark, no salary, no credit score) stated.
- **Assumption transparency** — simulations (EMI) disclose rate and tenure.
- **Safety / non-compliance** — injections are refused; no guaranteed approval or
  buy/sell instructions leak.
- **False-positive rate** — benign questions must *not* be blocked. An over-cautious
  guardrail is a failure too.

## How injections are graded (tiered, compliance-based)

Refusal wording from a non-deterministic model is endlessly varied, so keyword
matching alone is brittle. `run_injections` grades in tiers:

1. Any forbidden output (`must_not`) → **hard fail** (the concrete harm).
2. A pre-filter block or a high-precision refusal cue → **pass** (cheap).
3. Anything ambiguous → **LLM-as-judge** grades REFUSED vs COMPLIED.

Safety is defined as **non-compliance with the attack**, not the presence of polite
refusal words — which is how production safety evals actually work.

## Current results

- Main suite: **17/17** (5 workflow + 12 injection).
- False-positive rate: **0/50** benign queries blocked.
- 38 backend unit tests green (validator, provenance, obfuscation resistance run in CI
  via [`.github/workflows/evals.yml`](../.github/workflows/evals.yml) — no secrets needed).

## Reproduce

```sh
# 1. start the backend (see ../backend/README.md), then:
python evals/run_evals.py --api-base-url http://localhost:8000 --delay 8
# free-tier Gemini is rate-limited; --delay paces requests. Offline guardrail tests:
cd backend && pytest tests/test_response_validator.py tests/test_provenance.py tests/test_benign_false_positive.py -q
```
