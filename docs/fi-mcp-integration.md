# Fi MCP Dev Integration

> **Status:** confirmed facts captured here; full setup guide lands in **Issue #2**.

How FinSight Agent integrates the upstream [`epiFi/fi-mcp-dev`](https://github.com/epiFi/fi-mcp-dev)
server as its MCP (financial context) layer.

## Confirmed facts (verified against the upstream repo on 2026-06-24)

- **Language / run:** Go server (Go 1.23+). Start with `FI_MCP_PORT=8080 go run .`; serves on `http://localhost:8080`.
- **MCP endpoint:** `/mcp/stream`. Also exposes `/mockWebPage` (login page), `/login`, `/static/`.
- **Auth:** dummy login by allowed phone number (the directory names under `test_data_dir/`). Any OTP/passcode is accepted. Sessions are held **in memory** for the server run.
- **Session header:** `Mcp-Session-Id`. Custom session IDs **must** be prefixed with `mcp-session-`
  (e.g. `mcp-session-3ef38b37-...`). An unprefixed UUID is rejected as invalid.
- **Session model:** one session = one MCP client↔server connection, logged in once. Multi-agent
  setups must **share a single common session ID** rather than each agent opening its own.
- **`skip_auth` branch** exists for bypassing login (upstream issue #3); not recommended.
- **Server-side guardrails (baked into the server's MCP instructions):** do not estimate or
  extrapolate data; clearly state missing data; spending-analysis data is not offered via MCP;
  historical bank/stock transactions and salary may be absent.

## Tools exposed (confirmed)

| Tool | Returns |
|------|---------|
| `fetch_net_worth` | Net worth: asset values, liability values, total net worth |
| `fetch_credit_report` | Credit score, loan details, account history, date of birth |
| `fetch_epf_details` | EPF account / UAN details |
| `fetch_mf_transactions` | Mutual fund transactions |
| `fetch_bank_transactions` | Bank transactions |
| `fetch_stock_transactions` | Indian / US stock transactions |

## Synthetic personas (confirmed — `test_data_dir/<phone>/`)

| Phone | Persona / scenario |
|-------|--------------------|
| 1111111111 | No assets connected (savings balance only) |
| 2222222222 | All assets connected; large MF portfolio (9 funds) |
| 3333333333 | All assets connected; small MF portfolio (1 fund) |
| 4444444444 | All assets; 2 UANs, 3 banks, transactions for 2 accounts |
| 5555555555 | All assets except credit score |
| 6666666666 | All assets except bank account; large MF portfolio |
| 7777777777 | Debt-Heavy Low Performer |
| 8888888888 | SIP Samurai |
| 9999999999 | Fixed Income Fanatic |
| 1010101010 | Precious Metal Believer |
| 1212121212 | Dormant EPF Earner |
| 1313131313 | Balanced Growth Tracker |
| 1414141414 | Salary Sinkhole |
| 2020202020 | Starter Saver |
| 2121212121 | Dual Income Dynamo |
| 2525252525 | Live-for-Today Spender |

## To be documented in Issue #2

- Step-by-step local setup (clone into `external/`, `go mod tidy`, run).
- The login handshake and how the backend captures `login_url`.
- Worked `curl` and Python/ADK client examples against a live local server.
