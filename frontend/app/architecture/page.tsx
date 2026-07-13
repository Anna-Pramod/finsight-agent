// "How it works" — explained for a person first, with a technical section below.
const steps: [string, string][] = [
  ["Your data stays organised in one place", "FinSight reads from a structured record of your financial life — bank transactions, investments, retirement fund, credit report — through a controlled, permission-based connection. It sees only what's connected, and you can always see what it saw."],
  ["It reads before it speaks", "When you ask a question, FinSight first decides which of your records are relevant, reads them, and only then writes an answer. It never answers from general knowledge about 'people like you'."],
  ["Every answer is checked before you see it", "A separate safety layer reviews each answer: no promises, no product pushing, no buy/sell instructions, and no numbers that didn't come from your records. If something's off, the answer is stopped."],
  ["You see the working", "Under every answer is the list of records used, anything that was missing, and any assumptions made. Trust comes from showing the working, not asking for it."],
];

const tech: [string, string][] = [
  ["Data layer", "A Model Context Protocol (MCP) server exposes six read-only financial data tools per profile."],
  ["Reasoning layer", "A Google ADK agent (Gemini) plans which tools to call, reads the results, and drafts a structured answer: observation, risk, next step."],
  ["Safety layer", "Deterministic pre- and post-checks block prompt injection, ungrounded figures, and advice-like phrasing — independent of the model."],
  ["Delivery", "A FastAPI service on Google Cloud Run, with this interface served as a static web app."],
];

export default function ArchitecturePage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-xl font-semibold">How FinSight works</h1>
      <p className="mt-2 text-sm leading-relaxed" style={{ color: "var(--ink-2)" }}>
        No magic, no black box — just a careful pipeline from your question to an honest answer.
      </p>
      <ol className="mt-6 space-y-3">
        {steps.map(([title, body], i) => (
          <li key={title} className="card p-5">
            <h3 className="text-sm font-semibold">{i + 1}. {title}</h3>
            <p className="mt-1 text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>{body}</p>
          </li>
        ))}
      </ol>

      <details className="mt-10">
        <summary className="cursor-pointer text-sm font-semibold" style={{ color: "var(--ink-2)" }}>
          For the technically curious
        </summary>
        <div className="mt-3 grid gap-3 sm:grid-cols-2">
          {tech.map(([title, body]) => (
            <div key={title} className="card p-4">
              <h4 className="text-xs font-semibold">{title}</h4>
              <p className="mt-1 text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>{body}</p>
            </div>
          ))}
        </div>
        <p className="mt-3 text-xs" style={{ color: "var(--ink-muted)" }}>
          The full source is open —{" "}
          <a className="underline" href="https://github.com/Anna-Pramod/finsight-agent">
            github.com/Anna-Pramod/finsight-agent
          </a>.
        </p>
      </details>
    </main>
  );
}
