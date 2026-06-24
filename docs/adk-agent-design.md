# ADK Agent Design

> **Status:** placeholder — expanded in Issues #6, #11–#14.

How the Google ADK agent layer is structured.

This document will cover:

- The root finance agent and its six specialist sub-agents (Net Worth, Loan Affordability, SIP Performance, Debt Risk, Anomaly, Safety & Grounding).
- How agents are wired to Fi MCP Dev via a single shared `MCPToolset` / session.
- Instruction design for each agent and how grounding is enforced.
- Delegation strategy: when the root agent routes to which specialist.
- Confirmed upstream example (`LlmAgent` + `MCPToolset` + `StreamableHTTPConnectionParams`) vs our multi-agent extension.
