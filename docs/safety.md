# Safety & Grounding

> **Status:** placeholder — expanded in Issue #7.

FinSight Agent is **not a financial advisor**. This document defines the safety model.

This document will cover:

- Hard rules: no regulated advice, no guaranteed loan approval, no buy/sell instructions.
- Grounding: answer only from MCP data; clearly disclose missing data; show assumptions for simulations.
- Output structure: separate observation, risk, and suggested next step; always include a disclaimer.
- Prompt-injection defence and how untrusted tool/data content is treated as data, not instructions.
- How the upstream server's own data-boundary rules are surfaced and reinforced by our validator.
