# Architecture

End-to-end design of FinSight Agent: how a plain-English money question becomes a
grounded, audited answer.

## Request lifecycle

```
Browser (Next.js, GitHub Pages)
   │  POST /chat { persona, question }
   ▼
FastAPI backend (Cloud Run)
   │  1. resolve persona name → data source
   │  2. PRE-FILTER: deterministic prompt-injection check  ─→ blocked? return refusal (0 tokens)
   │  3. open tool trace recorder (captures every payload)
   ▼
Agent turn (Google ADK LlmAgent on Gemini)
   │  4. route question → specialist focus, build instruction
   │  5. model decides which of 6 tools to call
   ▼
Fi MCP data layer (in-process local transport, or live fi-mcp-dev over HTTP)
   │  6. returns per-persona financial JSON
   ▼
Agent drafts structured answer (observation / risk / next step + assumptions)
   ▼
POST-HOC VALIDATOR
   │  7. block forbidden phrasing (guarantees, buy/sell)
   │  8. block ungrounded figures (rupees quoted with no tool call)
   │  9. numeric provenance: verify each ₹ figure against retrieved payloads
   ▼
Audit log ← records tools used, missing data, blocked flag, unverified figures
   │
   ▼
ChatResponse → frontend renders answer + "Data we checked" trace
```

## Components

| Layer | Tech | Responsibility |
|-------|------|----------------|
| Frontend | Next.js + TS + Tailwind, static-exported to GitHub Pages | Profile picker, chat, dashboard, tool-trace panel. Calls the backend via `NEXT_PUBLIC_API_BASE_URL`. No secrets, no server. |
| Backend | FastAPI (Python 3.12) on Cloud Run | `/chat`, `/personas`, `/snapshot`, `/audit`, `/health`. Owns the MCP session, safety validation, audit trail. |
| Agent | Google ADK `LlmAgent` + Gemini | Plans tool calls, reads results, drafts the structured answer. |
| Data | Fi MCP layer — six `fetch_*` tools | Per-persona financial JSON (net worth, credit, EPF, MF, bank, stocks). |

## The agent: one routed agent, not six sub-agents (honest description)

The README's diagram shows six "specialists" — that is the *conceptual* decomposition.
The **actual implementation is a single `LlmAgent`** ([`app/agents/root_agent.py`](../backend/app/agents/root_agent.py))
whose instruction is composed per request:

- A cheap keyword router ([`instructions.route_focus`](../backend/app/agents/instructions.py))
  maps the question to one focus — net worth, loan affordability, SIP, debt risk,
  anomaly, or general.
- `build_instruction(question)` = the shared root instruction (safety rules + the
  six tools + the output schema) **plus** that one focus block.
- The single agent is given all six tools and decides which to call.

So "specialist" = a routed instruction slice, **not** a separate agent process or a
delegating multi-agent graph. This is a deliberate simplification: it gives focused
prompting without the latency and token cost of true sub-agent delegation, and it is
honest to say so in an interview. A genuine multi-agent version (root agent that
delegates to child `LlmAgent`s over a shared MCP session) is the natural next step.

## The MCP layer: one interface, two transports

The agent talks to a `FiMcpClient` over a `Transport` interface, so the same agent
code runs against either:

- **`LocalDataTransport`** (`FI_MCP_MODE=local`, the default and what the hosted demo
  uses) — serves the upstream `fi-mcp-dev` persona JSON in-process. No Go server, so
  the whole backend deploys as one Cloud Run service.
- **`HttpStreamTransport`** (`FI_MCP_MODE=http`) — talks to a running `fi-mcp-dev` Go
  server over `/mcp/stream` with a shared `mcp-session-…` id.

The transport is wrapped by a `ToolTraceRecorder` that captures every call and its
raw payload — feeding both the user-facing trace panel and the provenance check.

## Response schema

Every answer is structured, never free text:

```jsonc
{
  "observation": "what the data shows, with real figures",
  "risk": "an evidenced risk, or null",
  "suggested_next_step": "an educational step, or null",
  "assumptions": ["every assumption used, e.g. the EMI rate/tenure"],
}
```

plus `tools_called`, `missing_data`, `blocked`, and a `disclaimer` on the envelope.

## Deployment

- Frontend: GitHub Actions builds the static export (`basePath=/finsight-agent`) and
  publishes to GitHub Pages.
- Backend: `gcloud run deploy --source backend` builds the container (which clones the
  persona data at build time) and deploys to Cloud Run.
- See [`deployment.md`](deployment.md) for the exact commands and the model-quota notes.
