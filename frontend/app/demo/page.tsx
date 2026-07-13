"use client";
// Interactive demo: persona selector + dashboard + grounded chat + tool trace.
import { useEffect, useState } from "react";
import ChatPanel from "@/components/ChatPanel";
import FinanceDashboard from "@/components/FinanceDashboard";
import PersonaSelector from "@/components/PersonaSelector";
import { getPersonas, getSnapshot } from "@/lib/api";
import type { Persona, Snapshot } from "@/lib/types";

export default function DemoPage() {
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [selected, setSelected] = useState("SIP Samurai");
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPersonas().then(setPersonas).catch((e) => setError(String(e)));
  }, []);

  useEffect(() => {
    setSnapshot(null);
    getSnapshot(selected).then(setSnapshot).catch((e) => setError(String(e)));
  }, [selected]);

  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="text-xl font-semibold">Live demo</h1>
      <p className="mt-1 text-sm" style={{ color: "var(--ink-2)" }}>
        Pick a synthetic persona, then ask the agent about their money. Every answer shows
        which tools ran and what data was missing.
      </p>
      {error && (
        <p className="mt-4 text-sm" style={{ color: "var(--status-critical)" }}>
          Backend unreachable: {error}
        </p>
      )}
      <div className="mt-6 grid gap-6 lg:grid-cols-[320px,1fr]">
        <div className="space-y-4">
          <PersonaSelector personas={personas} selected={selected} onSelect={setSelected} />
          {snapshot ? (
            <FinanceDashboard snapshot={snapshot} />
          ) : (
            !error && <p className="animate-pulse text-sm" style={{ color: "var(--ink-muted)" }}>Loading snapshot…</p>
          )}
        </div>
        <ChatPanel key={selected} persona={selected} />
      </div>
    </main>
  );
}
