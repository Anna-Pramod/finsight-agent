# Architecture

> **Status:** placeholder — expanded in later issues.

End-to-end design of FinSight Agent: how the frontend, backend, agent layer, and MCP layer fit together.

This document will cover:

- The full request lifecycle from a user question to a grounded, audited answer.
- Component responsibilities: Next.js frontend, FastAPI backend, ADK agent layer, Fi MCP Dev.
- How one shared MCP session is owned by the backend and reused across all specialist agents.
- Data flow and response schema (observation vs risk vs suggested next step).
- Sequence diagrams for each MVP workflow.
