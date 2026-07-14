"use client";
// The FinSight app. First visit: pick a profile (card grid). Then: overview + chat,
// with a compact profile chip to switch at any time.
import { useEffect, useState } from "react";
import ChatPanel from "@/components/ChatPanel";
import FinanceDashboard from "@/components/FinanceDashboard";
import ProfilePicker from "@/components/ProfilePicker";
import { getPersonas, getSnapshot } from "@/lib/api";
import { PROFILE_BLURBS, PROFILE_EMOJI } from "@/lib/friendly";
import type { Persona, Snapshot } from "@/lib/types";

export default function DemoPage() {
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    getPersonas().then(setPersonas).catch(() => setError(true));
  }, []);

  useEffect(() => {
    if (!selected) return;
    setSnapshot(null);
    getSnapshot(selected).then(setSnapshot).catch(() => setError(true));
  }, [selected]);

  if (error) {
    return (
      <main className="mx-auto max-w-6xl px-4 py-8">
        <p className="rounded-md px-3 py-2 text-sm" style={{ background: "var(--page)", color: "var(--status-critical)" }}>
          FinSight is taking a moment to wake up. Please refresh in a few seconds.
        </p>
      </main>
    );
  }

  if (!selected) {
    return (
      <main className="mx-auto max-w-4xl px-4 py-10">
        {personas.length === 0 ? (
          <div className="card animate-pulse p-5 text-sm" style={{ color: "var(--ink-muted)" }}>
            Waking FinSight up…
          </div>
        ) : (
          <ProfilePicker personas={personas} onSelect={setSelected} />
        )}
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span aria-hidden className="text-3xl">{PROFILE_EMOJI[selected] ?? "🙂"}</span>
          <div>
            <h1 className="text-lg font-semibold leading-tight">{selected}</h1>
            <p className="text-xs" style={{ color: "var(--ink-muted)" }}>
              {PROFILE_BLURBS[selected] ?? "Sample profile"}
            </p>
          </div>
        </div>
        <button
          onClick={() => setSelected(null)}
          className="rounded-lg border px-3 py-1.5 text-xs hover:opacity-80"
          style={{ borderColor: "var(--hairline)", color: "var(--ink-2)" }}
        >
          ↩ Switch profile
        </button>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[340px,1fr]">
        <div className="space-y-4">
          {snapshot ? (
            <FinanceDashboard snapshot={snapshot} />
          ) : (
            <div className="card animate-pulse p-4 text-sm" style={{ color: "var(--ink-muted)" }}>
              Fetching this profile's accounts…
            </div>
          )}
        </div>
        <ChatPanel key={selected} persona={selected} />
      </div>
    </main>
  );
}
