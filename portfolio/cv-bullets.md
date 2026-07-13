# CV bullets

Pick 3–4 per application; lead with the one that matches the job description.
All claims are verifiable in the repo (tests, evals, CI) and the live product.

## For AI / GenAI engineer roles

- Built and shipped **FinSight**, a live agentic-AI personal-finance product
  (Next.js · FastAPI · Google ADK/Gemini · MCP): a tool-calling agent answers
  natural-language money questions grounded exclusively in per-user financial
  records, with the tool trace surfaced to the user on every answer.
  *(Live: anna-pramod.github.io/finsight-agent)*
- Designed a **three-layer safety architecture** for LLM output in a regulated
  domain — instruction-level rules, deterministic prompt-injection pre-filter, and
  a post-hoc validator blocking ungrounded figures and advice-like phrasing —
  verified by an automated eval suite (8/8: tool-selection, assumption disclosure,
  missing-data disclosure, 3 injection refusals).
- Implemented the **grounding contract** end-to-end: answers must cite only
  tool-retrieved data, disclose missing records, and enumerate every simulation
  assumption (e.g. EMI rate/tenure) — turning "trust me" AI into "check me" AI.
- Engineered around **free-tier LLM quotas** in production: empirically probed
  model availability (models-list API proved unreliable), selected the only viable
  model, and added exception-tree-aware retry/backoff so transient 429/503s never
  reach users.

## For backend / full-stack roles

- Shipped a **single-service Cloud Run backend** (FastAPI, Python 3.12) exposing
  chat, personas, deterministic snapshot, and audit APIs; 28 pytest tests run
  hermetically in CI by swapping the MCP transport for an in-process data layer —
  no live LLM or Go server needed in the pipeline.
- Built a **static-export Next.js frontend** deployed via GitHub Actions to GitHub
  Pages, with a validated, colorblind-safe data-viz palette and plain-language UX
  writing throughout (zero technical identifiers leak to the UI).

## One-liner (LinkedIn headline / summary)

Built FinSight — a live AI agent that answers questions about your money from your
own records, shows exactly which data it used, and refuses to cross into financial
advice. Google ADK · Gemini · MCP · FastAPI · Next.js.
