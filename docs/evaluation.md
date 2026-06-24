# Evaluation

> **Status:** placeholder — expanded in Issues #21–#22.

How FinSight Agent's quality, grounding, and safety are measured.

This document will cover:

- The evaluation datasets in `evals/` (query set, expected tool calls, prompt-injection set).
- The scoring rubric: grounding, tool-call correctness, disclosure of missing data, safety.
- How `evals/run_evals.py` executes the suite and reports pass/fail.
- Prompt-injection test methodology and acceptance thresholds.
- How results feed back into agent instruction and validator improvements.
