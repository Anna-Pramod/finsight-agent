"""FinSight Agent — evaluation runner.

Loads the .jsonl datasets, sends each query to the backend, and scores the
responses against expected tool calls and the rubric in rubric.md.

Status: placeholder (scaffold). Implemented in Issues #21-#22.

Planned usage:
    python evals/run_evals.py --api-base-url http://localhost:8000
"""


def main() -> None:
    # TODO(#21): load datasets, call the backend, score, and print a report.
    raise SystemExit("run_evals.py is a scaffold placeholder (Issues #21-#22).")


if __name__ == "__main__":
    main()
