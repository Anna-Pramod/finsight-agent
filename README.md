# FinSight Agent

> A full-stack agentic fintech assistant built with Fi MCP Dev, Google ADK, Vertex AI, FastAPI, and Next.js.

FinSight Agent is a solo, portfolio-grade Agentic AI project that lets a user *talk to their own money*. It connects a structured, user-controlled financial data layer (a Fi-style **MCP** server) to a reasoning agent (**Google ADK + Gemini/Vertex AI**), exposes it through a clean **FastAPI** backend, and presents it in a recruiter-friendly **Next.js** demo — with safety, auditability, and visible tool calls as first-class features.

This is **not a generic chatbot**. Every answer is grounded in tool-retrieved financial data, every tool call is visible, and the agent is explicitly *not* a financial advisor.

---

## Table of contents

1. [What FinSight Agent is](#what-finsight-agent-is)
2. [Why this project exists](#why-this-project-exists)
3. [Why MCP matters](#why-mcp-matters)
4. [Why Fi MCP Dev](#why-fi-mcp-dev)
5. [Why Google ADK + Gemini](#why-google-adk--gemini)
6. [Architecture](#architecture)
7. [Hosting plan](#hosting-plan)
8. [Safety note](#safety-note)
9. [Confirmed facts vs design decisions](#confirmed-facts-vs-design-decisions)
10. [Roadmap](#roadmap)
11. [Repository layout](#repository-layout)
12. [Status](#status)

---

## What FinSight Agent is

FinSight Agent answers deeply personalised financial questions such as:

- *"How is my net worth growing?"*
- *"Can I afford a ₹50L home loan?"*
- *"Which SIPs underperformed the market?"*
- *"What should I worry about in my finances?"*

It does this by orchestrating specialist sub-agents over a structured financial context, rather than guessing from a language model's parametric memory. The user always sees **which tools ran**, **what data was used**, and **what data was missing**.

## Why this project exists

This project is inspired by the **"Let AI speak to your money"** problem statement (Google Agentic AI / Fi Money hackathon theme).

The core insight: general-purpose AI can answer generic finance questions, but it **cannot reason about *your* money** without structured, secure, user-controlled access to your real financial footprint — which is scattered across banks, mutual funds, stocks, EPF, credit reports, loans, and liabilities. The missing layer is **infrastructure that connects that footprint to an AI agent** while respecting privacy and user control.

FinSight Agent is a focused, well-engineered demonstration of that layer, built to showcase fintech AI, agentic AI, generative AI, backend, and applied-AI engineering skills in one coherent project.

## Why MCP matters

**MCP (Model Context Protocol)** is a standard way for AI systems to connect to tools and structured data sources. In FinSight Agent, MCP is the **financial context layer**: it exposes finance tools (net worth, credit report, EPF, mutual funds, bank transactions) to the agent through a consistent, auditable interface, instead of bespoke per-source glue code. This is what makes the agent's answers *grounded* and its data access *inspectable*.

## Why Fi MCP Dev

We build on the official [`epiFi/fi-mcp-dev`](https://github.com/epiFi/fi-mcp-dev) repository as the upstream Fi-style MCP server. It is a minimal, hackathon-ready mock of the production Fi MCP server: it serves **dummy financial data** from static JSON files and uses a **simplified login flow**, which makes it safe for non-production experimentation. See [`external/README.md`](external/README.md) and [`docs/fi-mcp-integration.md`](docs/fi-mcp-integration.md).

## Why Google ADK + Gemini

**Google ADK (Agent Development Kit)** orchestrates the agent: a root finance agent that delegates to specialist sub-agents and calls MCP tools. **Gemini / Vertex AI** performs the reasoning over retrieved financial context. The upstream repo ships a working ADK + MCP `MCPToolset` example, which we extend into a multi-agent, safety-validated system exposed via FastAPI.

## Architecture

```
                ┌──────────────────────────────────────────────┐
   Browser  ──▶ │  Next.js + TypeScript + Tailwind (GitHub Pages)│
                │  Persona selector · Chat · Dashboard ·         │
                │  Tool-trace panel · Risk cards · Export        │
                └───────────────────────┬──────────────────────┘
                                         │  NEXT_PUBLIC_API_BASE_URL
                                         ▼
                ┌──────────────────────────────────────────────┐
                │  FastAPI backend (Google Cloud Run)            │
                │  Chat API · Persona mapping · Audit logger ·   │
                │  Safety validator · Response schemas           │
                └───────────────────────┬──────────────────────┘
                                         ▼
                ┌──────────────────────────────────────────────┐
                │  Google ADK root agent (Gemini / Vertex AI)    │
                │  Net Worth · Loan Affordability · SIP ·        │
                │  Debt Risk · Anomaly · Safety & Grounding      │
                └───────────────────────┬──────────────────────┘
                                         │  one shared mcp-session-… per demo session
                                         ▼
                ┌──────────────────────────────────────────────┐
                │  Fi MCP Dev (epiFi/fi-mcp-dev) — /mcp/stream   │
                │  fetch_net_worth · fetch_credit_report ·       │
                │  fetch_epf_details · fetch_mf_transactions ·   │
                │  fetch_bank_transactions · fetch_stock_…       │
                └──────────────────────────────────────────────┘
```

Full detail lives in [`docs/architecture.md`](docs/architecture.md) and [`docs/adk-agent-design.md`](docs/adk-agent-design.md).

## Hosting plan

- **Frontend / portfolio demo → GitHub Pages.** The Next.js app is exported as a static site (`output: 'export'`) and served from GitHub Pages. GitHub Pages hosts **static assets only**.
- **Backend (FastAPI + ADK) → Google Cloud Run.** The agent backend is a long-running service and is deployed separately to a backend-capable platform. The frontend reaches it via the `NEXT_PUBLIC_API_BASE_URL` environment variable.
- **MCP layer.** For local development, the official `fi-mcp-dev` Go server runs alongside the backend. For the public demo, we use the same data shape and persona mapping behind a controlled backend session (see [Safety note](#safety-note) and [`docs/deployment.md`](docs/deployment.md)).

## Safety note

**The public demo uses dummy data only.** All financial figures come from the synthetic personas shipped in `fi-mcp-dev`'s `test_data_dir/`. No real user data is ever connected in the hosted demo.

FinSight Agent is **not a financial advisor**. The system is designed to:

- answer only from available MCP data and clearly disclose what is missing;
- show assumptions for any simulation (e.g. assumed interest rate / tenure for an EMI);
- distinguish *observation* from *risk* from *suggested next step*;
- avoid guaranteeing loan approval or issuing buy/sell instructions;
- block prompt-injection attempts;
- always show which tools and data were used.

Details in [`docs/safety.md`](docs/safety.md).

## Confirmed facts vs design decisions

This project deliberately separates what is **verified from the upstream repo** from what is **our own design**. (Upstream facts below were verified by inspecting `epiFi/fi-mcp-dev` on 2026-06-24.)

**Confirmed facts (from `epiFi/fi-mcp-dev`):**

- It is a **Go server** (Go 1.23+), run with `FI_MCP_PORT=8080 go run .`, serving on `http://localhost:8080`.
- The MCP endpoint is **`/mcp/stream`**; it also exposes `/mockWebPage` (login page), `/login`, and `/static/`.
- Authentication is a **dummy login** by allowed phone number (the directory names under `test_data_dir/`); any OTP/passcode is accepted. Sessions are stored **in memory** for the server run.
- The session header is **`Mcp-Session-Id`**, and any custom session ID **must be prefixed with `mcp-session-`**.
- A session is a **one-to-one** MCP client↔server connection and only needs to log in once; multi-agent setups must **share one common session ID**.
- It exposes **six tools**: `fetch_net_worth`, `fetch_credit_report`, `fetch_epf_details`, `fetch_mf_transactions`, `fetch_bank_transactions`, `fetch_stock_transactions`.
- It ships **16 synthetic personas** (see [`docs/fi-mcp-integration.md`](docs/fi-mcp-integration.md)).
- The server itself instructs clients **not to estimate or extrapolate** data, to **clearly state missing data**, and notes that **historical bank/stock transactions and salary may be absent**.

**Design decisions (ours, proposed):**

- Multi-agent decomposition (root + 6 specialists) using ADK.
- A FastAPI session manager that owns one shared `mcp-session-…` per demo session.
- A response-validator / safety-grounding layer on top of the model output.
- A persona-mapping layer so the frontend can select a persona by name rather than phone number.

**Assumptions / limitations (to revisit):** exact ADK + MCP wiring versions, Vertex vs API-key auth, and the hosted-demo session strategy are tracked as open questions in the relevant `docs/` files and GitHub issues.

## Roadmap

Tracked as GitHub issues (#1–#25):

| Phase | Issues | Focus |
|-------|--------|-------|
| Scaffold | #1–#2 | Repo structure, docs, Fi MCP Dev setup guide |
| Backend core | #3–#10 | FastAPI skeleton, health, MCP session manager, ADK root agent, safety, personas, chat API, audit/tool-trace |
| Workflows | #11–#14 | Net worth growth, loan affordability, SIP performance, financial risk |
| Frontend | #15–#20 | Next.js skeleton, Pages export, persona selector, chat, tool-trace panel, dashboard |
| Quality | #21–#22 | Evaluation dataset, prompt-injection tests |
| Ship | #23–#25 | Deployment docs, portfolio case study, demo video + README polish |

## Repository layout

```text
finsight-agent/
├── README.md            # this file
├── LICENSE              # MIT
├── docs/                # architecture, integration, safety, eval, deployment, case study
├── external/            # how epiFi/fi-mcp-dev is used (the MCP foundation)
├── backend/             # FastAPI + ADK agent backend (deploys to Cloud Run)
├── frontend/            # Next.js + TS + Tailwind (deploys to GitHub Pages)
├── evals/               # query sets, expected tool calls, prompt-injection tests, rubric
├── portfolio/           # demo script, LinkedIn post, CV bullets, interview Q&A
└── .github/             # CI workflows, issue templates, PR template
```

## Status

🟢 **Functional end-to-end.** Backend (FastAPI + Google ADK + Gemini over the six Fi MCP tools), safety validator, audit/tool-trace, Next.js frontend, and the eval suite are implemented and tested (28 backend tests). The hosted demo serves the upstream persona data in-process (`FI_MCP_MODE=local`); point `FI_MCP_MODE=http` at a running `fi-mcp-dev` for the live Go server. Remaining: Cloud Run + GitHub Pages deployment (see `docs/deployment.md`).

---

*Built as a portfolio project. Inspired by the "Let AI speak to your money" problem statement. The MCP foundation is based on [`epiFi/fi-mcp-dev`](https://github.com/epiFi/fi-mcp-dev).*
