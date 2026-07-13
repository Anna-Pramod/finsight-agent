// About page — product voice, honest about what this preview is.
const beliefs: [string, string][] = [
  ["Money advice is broken", "Most 'advice' online is generic, and most apps that know your data use it to sell you things. There's very little that simply explains your own situation to you, clearly and honestly."],
  ["AI finally makes this possible — carefully", "Modern AI can read a full financial picture and explain it in plain language. But in finance, 'mostly right' isn't good enough — so FinSight is built to only speak from your actual records, admit what it doesn't know, and never cross into regulated advice."],
  ["Transparency is the product", "Every answer shows its sources, its assumptions, and its gaps. If an AI is going to talk about your money, you deserve to see its working. That principle shapes everything here."],
  ["What you're seeing today", "This is a working preview on realistic sample profiles — the full pipeline (data, reasoning, safety checks) is real; the accounts are not. Connecting real accounts safely is the obvious next chapter."],
];

export default function AboutPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-xl font-semibold">Why FinSight exists</h1>
      <p className="mt-2 text-sm leading-relaxed" style={{ color: "var(--ink-2)" }}>
        Everyone deserves a patient, honest explanation of their own money.
      </p>
      {beliefs.map(([title, body]) => (
        <section key={title} className="mt-6">
          <h2 className="text-sm font-semibold" style={{ color: "var(--accent)" }}>{title}</h2>
          <p className="mt-1 text-sm leading-relaxed" style={{ color: "var(--ink-2)" }}>{body}</p>
        </section>
      ))}
      <p className="mt-10 text-xs" style={{ color: "var(--ink-muted)" }}>
        Built by Anna Pramod. FinSight is open source —{" "}
        <a className="underline" href="https://github.com/Anna-Pramod/finsight-agent">
          see how it's made
        </a>.
      </p>
    </main>
  );
}
