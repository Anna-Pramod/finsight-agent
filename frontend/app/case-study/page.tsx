// Portfolio case study page (narrative version of docs/portfolio-case-study.md).
const sections: [string, string][] = [
  ["Problem", "General-purpose AI cannot reason about your money without structured, user-controlled access to your financial footprint. The missing layer is infrastructure connecting that footprint to an agent — safely."],
  ["Approach", "A Fi-style MCP server is the financial context layer; a Google ADK root agent (Gemini) calls its six tools; FastAPI owns sessions, safety validation, and audit; Next.js renders answers with full tool transparency."],
  ["Safety design", "Three layers: instruction-level rules, a deterministic pre-flight injection filter, and a post-hoc output validator that blocks advice-like phrasing and ungrounded figures. Every response carries a disclaimer and its tool trace."],
  ["Result", "Grounded persona-specific answers with visible tool calls, missing-data disclosure, EMI simulations with explicit assumptions, and refused injection attempts — deployed as a static frontend plus one Cloud Run service."],
];

export default function CaseStudyPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-xl font-semibold">Case study</h1>
      {sections.map(([title, body]) => (
        <section key={title} className="mt-6">
          <h2 className="text-sm font-semibold" style={{ color: "var(--accent)" }}>{title}</h2>
          <p className="mt-1 text-sm leading-relaxed" style={{ color: "var(--ink-2)" }}>{body}</p>
        </section>
      ))}
    </main>
  );
}
