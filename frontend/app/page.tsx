// Landing page: what FinSight Agent is and where to click.
import Link from "next/link";

const features = [
  ["Grounded answers", "Every figure comes from a tool call over connected data — never from model memory."],
  ["Visible tool trace", "Each answer shows exactly which MCP tools ran and what data was missing."],
  ["Safety validated", "Prompt-injection attempts are refused; advice-like output is blocked by a validator."],
  ["Multi-agent ADK", "A root Gemini agent routes to specialist focuses: net worth, loans, SIPs, risk."],
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-14">
      <h1 className="max-w-2xl text-3xl font-semibold tracking-tight">
        Talk to your money — with an agent that shows its work.
      </h1>
      <p className="mt-3 max-w-2xl text-sm leading-relaxed" style={{ color: "var(--ink-2)" }}>
        FinSight Agent is a full-stack agentic fintech demo: Google ADK + Gemini reasoning over a
        Fi-style MCP financial data layer, exposed through FastAPI and this Next.js app. Synthetic
        persona data only.
      </p>
      <div className="mt-6 flex gap-3">
        <Link
          href="/demo/"
          className="rounded-md px-4 py-2 text-sm font-medium text-white"
          style={{ background: "var(--accent)" }}
        >
          Try the demo
        </Link>
        <Link
          href="/architecture/"
          className="rounded-md border px-4 py-2 text-sm"
          style={{ borderColor: "var(--hairline)" }}
        >
          How it works
        </Link>
      </div>
      <div className="mt-12 grid gap-4 sm:grid-cols-2">
        {features.map(([title, body]) => (
          <div key={title} className="card p-4">
            <h3 className="text-sm font-semibold">{title}</h3>
            <p className="mt-1 text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>
              {body}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}
