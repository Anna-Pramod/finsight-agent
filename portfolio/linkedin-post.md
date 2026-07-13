# LinkedIn post

Post the video (see demo-script.md) with this text. Best time: Tue–Thu morning.

---

I got tired of AI that talks *about* money but can't talk about *your* money.

So I built FinSight — ask anything about your finances in plain English, and get an
answer grounded in your own records, with the receipts shown every time.

What makes it different:

🔍 Every answer lists exactly which records it read — and what was missing
📏 Every simulation discloses its assumptions (rate, tenure — nothing hidden)
🛡️ Try to jailbreak it into "guaranteed loan approval" and it refuses before
touching a single record
🚫 It explains and flags risks — it never pushes products or tells you to buy/sell

Under the hood: a Google ADK agent on Gemini, tool-calling over an MCP financial
data layer, a deterministic safety validator, FastAPI on Cloud Run, Next.js on
GitHub Pages. Tested (28 unit tests), eval'd (8/8 incl. three prompt-injection
attacks), open source.

Try it (sample profiles, no sign-up): https://anna-pramod.github.io/finsight-agent/
Source: https://github.com/Anna-Pramod/finsight-agent

Building AI for fintech is a trust problem before it's a model problem. This is my
take on earning that trust — I'd love feedback from folks working on agentic AI or
financial products.

#AgenticAI #Fintech #GenAI #LLM #BuildInPublic
