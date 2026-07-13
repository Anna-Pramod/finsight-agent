"use client";
// The FinSight app: profile picker + money overview + conversation.
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
    getPersonas().then(setPersonas).catch(() => setError("unreachable"));
  }, []);

  useEffect(() => {
    setSnapshot(null);
    getSnapshot(selected).then(setSnapshot).catch(() => setError("unreachable"));
  }, [selected]);

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-xl font-semibold">Hello 👋 Let's look at your money.</h1>
      <p className="mt-1 text-sm" style={{ color: "var(--ink-2)" }}>
        Pick a sample profile, then ask anything — FinSight answers from that profile's real records
        and always shows which ones it used.
      </p>
      {error && (
        <p className="mt-4 rounded-md px-3 py-2 text-sm" style={{ background: "var(--page)", color: "var(--status-critical)" }}>
          FinSight is taking a moment to wake up. Please refresh in a few seconds.
        </p>
      )}
      <div className="mt-6 grid gap-6 lg:grid-cols-[340px,1fr]">
        <div className="space-y-4">
          <PersonaSelector personas={personas} selected={selected} onSelect={setSelected} />
          {snapshot ? (
            <FinanceDashboard snapshot={snapshot} />
          ) : (
            !error && (
              <div className="card animate-pulse p-4 text-sm" style={{ color: "var(--ink-muted)" }}>
                Fetching this profile's accounts…
              </div>
            )
          )}
        </div>
        <ChatPanel key={selected} persona={selected} />
      </div>
    </main>
  );
}
