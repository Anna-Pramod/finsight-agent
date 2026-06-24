# external/ — the MCP foundation

FinSight Agent builds on the upstream **[`epiFi/fi-mcp-dev`](https://github.com/epiFi/fi-mcp-dev)**
server as its MCP (financial context) layer. We treat it as an **external dependency**: it is
**cloned here, not vendored/committed** into this repository (the path is git-ignored). This keeps
attribution clean and lets us pull upstream updates.

## What `fi-mcp-dev` is (confirmed, verified 2026-06-24)

A minimal, hackathon-ready mock of the production Fi MCP server, written in **Go**. It serves
**dummy financial data** from static JSON files in `test_data_dir/` and uses a **simplified login
flow**, making it safe for non-production demos and development.

- MCP endpoint: **`/mcp/stream`** (plus `/mockWebPage`, `/login`, `/static/`).
- Auth: dummy login by allowed **phone number** (the `test_data_dir/` directory names); any OTP works.
- Session header **`Mcp-Session-Id`**; custom IDs must be prefixed **`mcp-session-`**.
- Six tools: `fetch_net_worth`, `fetch_credit_report`, `fetch_epf_details`,
  `fetch_mf_transactions`, `fetch_bank_transactions`, `fetch_stock_transactions`.
- 16 synthetic personas (see [`../docs/fi-mcp-integration.md`](../docs/fi-mcp-integration.md)).

## How to obtain it locally

```sh
# from the repo root
git clone https://github.com/epiFi/fi-mcp-dev.git external/fi-mcp-dev
cd external/fi-mcp-dev
go mod tidy
FI_MCP_PORT=8080 go run .
# -> serves on http://localhost:8080 ; MCP stream at http://localhost:8080/mcp/stream
```

(`docker compose up` will also run it as the `fi-mcp` service — see the root `docker-compose.yml`.)

## How FinSight Agent uses it

- The FastAPI backend opens **one shared `mcp-session-…`** per demo session and reuses it across all
  ADK specialist agents (never one session per agent).
- Login-required responses (`{"status": "login_required", "login_url": ...}`) are handled
  gracefully and surfaced to the frontend when needed.
- The hosted public demo uses the **same data shape and persona mapping** but with dummy data only;
  no real financial accounts are ever connected.

## Attribution & licence

`fi-mcp-dev` is an upstream project by epiFi. Consult its repository for its own licence and terms.
FinSight Agent does not redistribute its source; it depends on it as described above.
