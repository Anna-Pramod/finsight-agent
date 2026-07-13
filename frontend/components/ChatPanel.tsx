"use client";
// Ask financial questions, view grounded structured answers with the tool trace.
import { useState } from "react";
import { postChat } from "@/lib/api";
import type { ChatResponse } from "@/lib/types";
import Disclaimer from "./Disclaimer";
import ToolTracePanel from "./ToolTracePanel";

const SAMPLES = [
  "How is my net worth growing?",
  "Can I afford a ₹50L home loan?",
  "Which SIPs underperformed the market?",
  "What should I worry about in my finances?",
];

interface Turn {
  question: string;
  response?: ChatResponse;
  error?: string;
}

export default function ChatPanel({ persona }: { persona: string }) {
  const [question, setQuestion] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>();

  async function ask(q: string) {
    if (!q.trim() || busy) return;
    setBusy(true);
    setTurns((t) => [...t, { question: q }]);
    setQuestion("");
    try {
      const res = await postChat(persona, q, sessionId);
      setSessionId(res.session_id);
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, response: res } : turn)));
    } catch (e) {
      setTurns((t) =>
        t.map((turn, i) => (i === t.length - 1 ? { ...turn, error: String(e) } : turn)),
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {SAMPLES.map((s) => (
          <button
            key={s}
            onClick={() => ask(s)}
            disabled={busy}
            className="rounded-full border px-3 py-1 text-xs hover:opacity-80 disabled:opacity-40"
            style={{ borderColor: "var(--hairline)", color: "var(--ink-2)" }}
          >
            {s}
          </button>
        ))}
      </div>

      {turns.map((turn, i) => (
        <div key={i} className="space-y-3">
          <p className="text-sm font-medium" style={{ color: "var(--accent)" }}>
            {turn.question}
          </p>
          {turn.error && (
            <p className="text-sm" style={{ color: "var(--status-critical)" }}>{turn.error}</p>
          )}
          {!turn.response && !turn.error && (
            <p className="animate-pulse text-sm" style={{ color: "var(--ink-muted)" }}>
              Running agent, calling tools…
            </p>
          )}
          {turn.response && (
            <div className="space-y-3">
              <div className="card p-4">
                {turn.response.blocked && (
                  <p className="mb-2 text-xs font-semibold" style={{ color: "var(--status-critical)" }}>
                    ⛔ Blocked by safety validator
                  </p>
                )}
                <p className="whitespace-pre-wrap text-sm leading-relaxed">
                  {turn.response.answer.observation}
                </p>
                {turn.response.answer.risk && (
                  <p className="mt-3 text-sm" style={{ color: "var(--ink-2)" }}>
                    <span className="font-semibold">Risk:</span> {turn.response.answer.risk}
                  </p>
                )}
                {turn.response.answer.suggested_next_step && (
                  <p className="mt-2 text-sm" style={{ color: "var(--ink-2)" }}>
                    <span className="font-semibold">Next step:</span>{" "}
                    {turn.response.answer.suggested_next_step}
                  </p>
                )}
                {turn.response.answer.assumptions.length > 0 && (
                  <ul className="mt-3 list-disc pl-5 text-xs" style={{ color: "var(--ink-muted)" }}>
                    {turn.response.answer.assumptions.map((a, j) => (
                      <li key={j}>{a}</li>
                    ))}
                  </ul>
                )}
                <Disclaimer text={turn.response.disclaimer} />
              </div>
              <ToolTracePanel calls={turn.response.tools_called} missing={turn.response.missing_data} />
            </div>
          )}
        </div>
      ))}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          ask(question);
        }}
        className="flex gap-2"
      >
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about your money…"
          className="flex-1 rounded-md border bg-transparent px-3 py-2 text-sm"
          style={{ borderColor: "var(--hairline)", background: "var(--surface-1)" }}
        />
        <button
          type="submit"
          disabled={busy || !question.trim()}
          className="rounded-md px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
          style={{ background: "var(--accent)" }}
        >
          Ask
        </button>
      </form>
    </div>
  );
}
