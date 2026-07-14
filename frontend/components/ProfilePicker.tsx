"use client";
// Welcome step: choose whose finances to explore, presented as people.
import type { Persona } from "@/lib/types";
import { FEATURED_PROFILES, PROFILE_BLURBS, PROFILE_EMOJI } from "@/lib/friendly";

interface Props {
  personas: Persona[];
  onSelect: (name: string) => void;
}

function Card({ p, big, onSelect }: { p: Persona; big?: boolean; onSelect: (n: string) => void }) {
  return (
    <button
      onClick={() => onSelect(p.name)}
      className={`card group flex w-full items-start gap-3 p-4 text-left transition-transform hover:-translate-y-0.5 hover:shadow-md ${big ? "sm:p-5" : ""}`}
    >
      <span aria-hidden className={big ? "text-3xl" : "text-2xl"}>
        {PROFILE_EMOJI[p.name] ?? "🙂"}
      </span>
      <span className="min-w-0">
        <span className="block text-sm font-semibold group-hover:underline">{p.name}</span>
        <span className="mt-0.5 block text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>
          {PROFILE_BLURBS[p.name] ?? p.scenario}
        </span>
      </span>
    </button>
  );
}

export default function ProfilePicker({ personas, onSelect }: Props) {
  const featured = FEATURED_PROFILES.map((n) => personas.find((p) => p.name === n)).filter(
    (p): p is Persona => Boolean(p),
  );
  const rest = personas.filter((p) => !FEATURED_PROFILES.includes(p.name));

  return (
    <div>
      <h2 className="text-lg font-semibold">Whose money shall we look at?</h2>
      <p className="mt-1 max-w-xl text-sm" style={{ color: "var(--ink-2)" }}>
        Each of these is a realistic sample profile with a full set of financial records —
        pick whoever sounds most like you, or most interesting.
      </p>

      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {featured.map((p) => (
          <Card key={p.name} p={p} big onSelect={onSelect} />
        ))}
      </div>

      {rest.length > 0 && (
        <details className="mt-5">
          <summary className="cursor-pointer text-sm font-medium" style={{ color: "var(--accent)" }}>
            Show {rest.length} more profiles
          </summary>
          <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {rest.map((p) => (
              <Card key={p.name} p={p} onSelect={onSelect} />
            ))}
          </div>
        </details>
      )}

      <p className="mt-6 text-xs" style={{ color: "var(--ink-muted)" }}>
        No sign-up, nothing to connect — these profiles exist so you can explore FinSight safely.
      </p>
    </div>
  );
}
