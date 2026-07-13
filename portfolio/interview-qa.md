# Interview Q&A prep

Real questions you're likely to get, with answers grounded in what you actually
built. Practice saying these out loud — 60–90 seconds each.

---

**"Walk me through the architecture."**
> Four layers. A Next.js static frontend on GitHub Pages calls a FastAPI service on
> Cloud Run. That service runs a Google ADK agent on Gemini which tool-calls into an
> MCP financial data layer — six read-only tools per user: net worth, credit report,
> EPF, mutual-fund, bank and stock transactions. The agent plans which tools a
> question needs, reads the results, and returns a structured answer — observation,
> risk, next step — which passes through a deterministic safety validator before the
> user sees it. Every response carries its tool trace, so the UI can show exactly
> which records were used.

**"How do you stop the LLM from hallucinating numbers?"**
> Three mechanisms, because no single one is enough. Instructions forbid estimating
> beyond tool data. Structurally, the agent can only see financial data through
> tools, so there's nothing else to quote. And post-hoc, a validator rejects any
> answer that quotes rupee figures when no tool was called. The eval suite tests
> this — including a profile with no connected assets, where the correct behaviour
> is to disclose what's missing rather than invent.

**"How do you handle prompt injection?"**
> Defence in depth. A deterministic regex pre-filter blocks obvious jailbreaks
> before any model or data access — cheap and unbypassable by clever wording of the
> model. The agent's instructions treat instructions embedded in data as data. And
> the output validator blocks advice-like or guarantee phrasing regardless of what
> caused it. My eval set includes three attack styles: direct override, persona
> hijack, and instructions smuggled inside the user's data. All three are refused —
> one pre-flight, two by the model with validator backup.

**"Why MCP instead of just calling APIs directly?"**
> Standardisation and auditability. MCP gives every data source one consistent,
> inspectable tool interface, so the agent layer doesn't accumulate bespoke glue
> code per bank or fund house — and the tool trace I show users falls out of the
> design for free. It also let me swap the transport: the same agent runs against a
> live MCP server over HTTP or an in-process data layer, which is how my tests stay
> hermetic and my Cloud Run deployment stays a single service.

**"What was the hardest engineering problem?"**
> Honestly? Free-tier LLM quotas in production. The models-list API said half a
> dozen models were available; in reality one returned 404 'not available to new
> users', another allowed 20 requests a day, and each agent turn makes 2–4 model
> calls. I ended up probing models empirically with real generation calls, chose the
> one viable model, added retry with backoff that walks Python exception groups
> (ADK wraps errors), and paced the eval suite. It taught me that LLM ops is as much
> about quota topology as prompts.

**"What would production need beyond this?"**
> Real account connections via an account aggregator, OAuth user identity, secrets
> in Secret Manager rather than env vars, persistent session and audit storage
> instead of in-memory, streaming responses for perceived latency, human-reviewed
> eval expansion, and a compliance review of the advice boundary — the validator
> enforces my rules; a regulator would have opinions about what those rules should be.

**"Why did you frame it as a product rather than a demo?"**
> Because the hard problems — grounding, transparency, refusing to overstep — only
> matter from the user's point of view. Framing it as a product forced plain-language
> UX for a layperson while keeping the engineering visible one click deeper. That's
> the actual job of applied AI in fintech: rigor underneath, clarity on top.
