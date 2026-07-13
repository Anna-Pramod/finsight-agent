// Architecture walkthrough (mirrors docs/architecture.md).
const layers = [
  ["Next.js frontend (GitHub Pages)", "Persona selector, chat, dashboard, tool-trace panel. Static export; calls the backend via NEXT_PUBLIC_API_BASE_URL."],
  ["FastAPI backend (Cloud Run)", "Chat API, persona mapping, shared MCP session manager, safety validator, audit log."],
  ["Google ADK agent (Gemini)", "Root finance agent routed to a specialist focus per question: net worth, loan affordability, SIP, debt risk, anomaly."],
  ["Fi MCP data layer", "Six fetch_* tools over 16 synthetic personas (epiFi/fi-mcp-dev data shape); local dummy-data transport in the hosted demo."],
];

export default function ArchitecturePage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-xl font-semibold">Architecture</h1>
      <p className="mt-2 text-sm" style={{ color: "var(--ink-2)" }}>
        A question flows down four layers and comes back as a grounded, audited answer.
      </p>
      <ol className="mt-6 space-y-3">
        {layers.map(([title, body], i) => (
          <li key={title} className="card p-4">
            <h3 className="text-sm font-semibold">
              {i + 1}. {title}
            </h3>
            <p className="mt-1 text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>
              {body}
            </p>
          </li>
        ))}
      </ol>
      <p className="mt-6 text-xs" style={{ color: "var(--ink-muted)" }}>
        Safety: prompt-injection pre-flight, forbidden-output post-check, grounding rule (figures
        require tool calls), and a disclaimer on every response.
      </p>
    </main>
  );
}
