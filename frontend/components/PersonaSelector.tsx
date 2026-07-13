"use client";
// Choose one of the 16 Fi MCP Dev demo personas (names only; phones stay server-side).
import type { Persona } from "@/lib/types";

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
        Demo persona
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
        <p className="mt-2 text-xs" style={{ color: "var(--ink-muted)" }}>
          {current.scenario}
        </p>
      )}
    </div>
  );
}
