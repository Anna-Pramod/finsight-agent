# Backend — FastAPI + Google ADK

The FinSight Agent backend. It exposes the agent over HTTP, owns the shared Fi MCP Dev session,
runs the ADK multi-agent system over Gemini/Vertex AI, validates responses for safety, and emits
an audit trail of tool calls. Deploys to **Google Cloud Run**.

> **Status:** scaffold only (Issue #1). Modules below are placeholders; logic lands per issue.

## Layout

```
app/
├── main.py            # FastAPI app entrypoint (Issue #3)
├── config.py          # Settings from environment (Issue #3)
├── api/               # HTTP routes
│   ├── health.py      # GET /health (Issue #4)
│   ├── chat.py        # POST /chat (Issue #9)
│   ├── personas.py    # GET /personas (Issue #8)
│   └── audit.py       # GET /audit (Issue #10)
├── agents/            # ADK agent layer
│   ├── root_agent.py        # root finance agent + specialists (Issue #6, #11–#14)
│   ├── instructions.py      # agent instructions incl. safety (Issue #7)
│   ├── session_manager.py   # one shared mcp-session per demo session (Issue #5)
│   └── response_validator.py# safety/grounding validation (Issue #7)
├── mcp/               # Fi MCP Dev integration
│   ├── fi_client.py         # MCP client wrapper (Issue #5–#6)
│   ├── persona_mapping.py   # persona name <-> phone number (Issue #8)
│   └── tool_trace.py        # capture which tools/data were used (Issue #10)
├── services/          # domain logic
│   ├── audit_logger.py      # structured audit log (Issue #10)
│   ├── risk_scoring.py      # debt/risk signals (Issue #14)
│   ├── affordability.py     # EMI / affordability maths (Issue #12)
│   └── export_service.py    # exportable insight (frontend export button)
└── schemas/           # Pydantic models
    ├── chat.py
    ├── finance.py
    └── audit.py
```

## Local development (later issues)

```sh
# create a virtualenv and install (exact tooling decided in Issue #3)
pip install -e .
uvicorn app.main:app --reload --port 8000
```

Requires a running Fi MCP Dev server (see `../external/README.md`) and a configured `.env`.
