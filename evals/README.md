# evals/ — evaluation suite

Measures FinSight Agent's grounding, tool-call correctness, missing-data disclosure, and safety.

> **Status:** scaffold with seed examples (Issue #1). The runner and full datasets land in
> Issues #21–#22. See [`../docs/evaluation.md`](../docs/evaluation.md).

## Files

- `test_queries.jsonl` — user questions tagged with a demo persona and target workflow.
- `expected_tool_calls.jsonl` — the MCP tools each query should trigger.
- `prompt_injection_tests.jsonl` — adversarial inputs and the required safe behaviour.
- `rubric.md` — scoring rubric.
- `run_evals.py` — executes the suite against the backend and reports results.

Each `.jsonl` file holds one JSON object per line (seed rows included as examples).
