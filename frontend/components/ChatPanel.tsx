"use client";
// Ask questions about your money; answers arrive as
// "what your data shows / worth watching / a step to consider".
import { useEffect, useRef, useState } from "react";
import { postChat } from "@/lib/api";
import type { ChatResponse } from "@/lib/types";
import ToolTracePanel from "./ToolTracePanel";

const SAMPLES = [
  "How is my net worth doing?",
  "Can I afford a ₹50L home loan?",
  "Which of my investments are lagging?",
  "What should I keep an eye on?",
];

const THINKING = [
  "Opening your accounts…",
  "Reading the numbers…",
  "Checking what's relevant…",
  "Putting it in plain words…",
];

interface Turn {
  question: string;
  response?: ChatResponse;
  error?: string;
}

function Thinking() {
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI((v) => (v + 1) % THINKING.length), 2600);
    return () => clearInterval(t);
  }, []);
  return (
    <div className="card flex items-center gap-3 p-4">
      <span className="inline-block h-2 w-2 animate-ping rounded-full" style={{ background: "var(--accent)" }} />
      <p className="text-sm" style={{ color: "var(--ink-2)" }}>{THINKING[i]}</p>
    </div>
  );
}

export default function ChatPanel({ persona }: { persona: string }) {
  const [question, setQuestion] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>();
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [turns]);

  async function ask(q: string) {
    if (!q.trim() || busy) return;
    setBusy(true);
    setTurns((t) => [...t, { question: q }]);
    setQuestion("");
    try {
      const res = await postChat(persona, q, sessionId);
      setSessionId(res.session_id);
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, response: res } : turn)));
    } catch {
      setTurns((t) =>
        t.map((turn, i) =>
          i === t.length - 1
            ? { ...turn, error: "We couldn't reach FinSight just now — it may be busy. Please try again in a moment." }
            : turn,
        ),
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-4">
      {turns.length === 0 && (
        <div className="card p-5">
          <h2 className="text-sm font-semibold">What would you like to know?</h2>
          <p className="mt-1 text-xs" style={{ color: "var(--ink-2)" }}>
            Ask in your own words, or start with one of these:
          </p>
        </div>
      )}
      <div className="flex flex-wrap gap-2">
        {SAMPLES.map((s) => (
          <button
            key={s}
            onClick={() => ask(s)}
            disabled={busy}
            className="rounded-full border px-3 py-1.5 text-xs hover:opacity-80 disabled:opacity-40"
            style={{ borderColor: "var(--hairline)", color: "var(--ink-2)" }}
          >
            {s}
          </button>
        ))}
      </div>

      {turns.map((turn, i) => (
        <div key={i} className="space-y-3">
          <div className="flex justify-end">
            <p
              className="max-w-[85%] rounded-2xl rounded-br-sm px-4 py-2 text-sm text-white"
              style={{ background: "var(--accent)" }}
            >
              {turn.question}
            </p>
          </div>
          {turn.error && (
            <p className="text-sm" style={{ color: "var(--status-critical)" }}>{turn.error}</p>
          )}
          {!turn.response && !turn.error && <Thinking />}
          {turn.response && (
            <div className="space-y-3">
              <div className="card p-5">
                {turn.response.blocked && (
                  <p className="mb-3 rounded-md px-3 py-2 text-xs font-medium"
                     style={{ background: "var(--page)", color: "var(--status-critical)" }}>
                    That request asked FinSight to break its safety rules, so it declined.
                  </p>
                )}
                <p className="text-[11px] font-semibold uppercase tracking-wider" style={{ color: "var(--accent)" }}>
                  What your data shows
                </p>
                <p className="mt-1 whitespace-pre-wrap text-sm leading-relaxed">
                  {turn.response.answer.observation}
                </p>
                {turn.response.answer.risk && (
                  <>
                    <p className="mt-4 text-[11px] font-semibold uppercase tracking-wider" style={{ color: "var(--status-warning)" }}>
                      Worth watching
                    </p>
                    <p className="mt-1 text-sm leading-relaxed" style={{ color: "var(--ink-2)" }}>
                      {turn.response.answer.risk}
                    </p>
                  </>
                )}
                {turn.response.answer.suggested_next_step && (
                  <>
                    <p className="mt-4 text-[11px] font-semibold uppercase tracking-wider" style={{ color: "var(--status-good)" }}>
                      A step to consider
                    </p>
                    <p className="mt-1 text-sm leading-relaxed" style={{ color: "var(--ink-2)" }}>
                      {turn.response.answer.suggested_next_step}
                    </p>
                  </>
                )}
                {turn.response.answer.assumptions.length > 0 && (
                  <div className="mt-4 rounded-md px-3 py-2" style={{ background: "var(--page)" }}>
                    <p className="text-[11px] font-medium" style={{ color: "var(--ink-2)" }}>
                      So you know, we assumed:
                    </p>
                    <ul className="mt-1 list-disc pl-4 text-xs leading-relaxed" style={{ color: "var(--ink-muted)" }}>
                      {turn.response.answer.assumptions.map((a, j) => (
                        <li key={j}>{a}</li>
                      ))}
                    </ul>
                  </div>
                )}
                <p className="mt-4 text-[11px]" style={{ color: "var(--ink-muted)" }}>
                  FinSight explains — it doesn't advise. Decisions stay yours.
                </p>
              </div>
              <ToolTracePanel calls={turn.response.tools_called} missing={turn.response.missing_data} />
            </div>
          )}
        </div>
      ))}
      <div ref={endRef} />

      <form
        onSubmit={(e) => {
          e.preventDefault();
          ask(question);
        }}
        className="sticky bottom-4 flex gap-2"
      >
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about your money — loans, savings, investments…"
          className="flex-1 rounded-lg border px-3 py-2.5 text-sm shadow-sm"
          style={{ borderColor: "var(--hairline)", background: "var(--surface-1)" }}
        />
        <button
          type="submit"
          disabled={busy || !question.trim()}
          className="rounded-lg px-5 py-2.5 text-sm font-medium text-white shadow-sm disabled:opacity-40"
          style={{ background: "var(--accent)" }}
        >
          Ask
        </button>
      </form>
    </div>
  );
}
