// Landing page — written for a person, not a recruiter.
import Link from "next/link";

const steps: [string, string, string][] = [
  ["1", "Pick a profile", "Choose one of our realistic sample profiles — a young saver, a heavy borrower, a disciplined investor — and see their full financial picture instantly."],
  ["2", "Ask in plain English", "“Can I afford a ₹50L home loan?” “Which of my investments are lagging?” No spreadsheets, no jargon."],
  ["3", "Get an honest answer", "Every answer shows what your data says, what to watch out for, and a sensible next step — plus exactly which of your records were used."],
];

const promises: [string, string][] = [
  ["Answers from your data, not guesses", "Every number in an answer comes straight from your accounts. If we didn't check it, we don't say it."],
  ["See the working, always", "Each answer lists the records it used — bank transactions, credit report, retirement fund — and tells you when something wasn't available."],
  ["Clarity, never pressure", "FinSight explains and flags risks. It will never push a product, promise a loan, or tell you to buy or sell anything."],
  ["Nothing hidden from you", "Assumptions are spelled out. If we estimate a monthly instalment, you'll see the interest rate and tenure we assumed."],
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-14">
      <p className="text-xs font-semibold uppercase tracking-widest" style={{ color: "var(--accent)" }}>
        Your money, finally explained
      </p>
      <h1 className="mt-2 max-w-2xl text-4xl font-semibold leading-tight tracking-tight">
        Ask anything about your money. Get a straight answer.
      </h1>
      <p className="mt-4 max-w-2xl text-base leading-relaxed" style={{ color: "var(--ink-2)" }}>
        Your financial life is scattered across banks, funds, loans and retirement accounts.
        FinSight pulls it together and answers your questions the way a patient, honest expert
        would — in plain language, showing its working every time.
      </p>
      <div className="mt-7 flex flex-wrap gap-3">
        <Link
          href="/demo/"
          className="rounded-lg px-5 py-2.5 text-sm font-medium text-white shadow-sm hover:opacity-90"
          style={{ background: "var(--accent)" }}
        >
          Try FinSight now — free
        </Link>
        <Link
          href="/architecture/"
          className="rounded-lg border px-5 py-2.5 text-sm hover:opacity-80"
          style={{ borderColor: "var(--hairline)" }}
        >
          How it works
        </Link>
      </div>
      <p className="mt-3 text-xs" style={{ color: "var(--ink-muted)" }}>
        No sign-up needed. The preview uses realistic sample profiles — your real accounts are never touched.
      </p>

      <section className="mt-16">
        <h2 className="text-lg font-semibold">Three steps to clarity</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-3">
          {steps.map(([n, title, body]) => (
            <div key={n} className="card p-5">
              <span
                className="inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-semibold text-white"
                style={{ background: "var(--accent)" }}
              >
                {n}
              </span>
              <h3 className="mt-3 text-sm font-semibold">{title}</h3>
              <p className="mt-1 text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>{body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-14">
        <h2 className="text-lg font-semibold">What makes FinSight different</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          {promises.map(([title, body]) => (
            <div key={title} className="card p-5">
              <h3 className="text-sm font-semibold">{title}</h3>
              <p className="mt-1 text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>{body}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
