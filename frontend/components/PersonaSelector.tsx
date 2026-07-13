"use client";
// Choose a sample profile — plain-language descriptions, no jargon.
import type { Persona } from "@/lib/types";
import { PROFILE_BLURBS } from "@/lib/friendly";

interface Props {
  personas: Persona[];
  selected: string;
  onSelect: (name: string) => void;
}

export default function PersonaSelector({ personas, selected, onSelect }: Props) {
  const current = personas.find((p) => p.name === selected);
  return (
    <div className="card p-4">
      <label className="mb-1 block text-xs font-medium" style={{ color: "var(--ink-2)" }}>
        Sample profile
      </label>
      <select
        className="w-full rounded-md border bg-transparent px-3 py-2 text-sm"
        style={{ borderColor: "var(--hairline)", color: "var(--ink-1)", background: "var(--surface-1)" }}
        value={selected}
        onChange={(e) => onSelect(e.target.value)}
      >
        {personas.map((p) => (
          <option key={p.name} value={p.name}>
            {p.name}
          </option>
        ))}
      </select>
      {current && (
        <p className="mt-2 text-xs leading-relaxed" style={{ color: "var(--ink-muted)" }}>
          {PROFILE_BLURBS[current.name] ?? current.scenario}
        </p>
      )}
      <p className="mt-2 text-[11px]" style={{ color: "var(--ink-muted)" }}>
        These are realistic sample profiles, so you can explore FinSight without connecting anything.
      </p>
    </div>
  );
}
