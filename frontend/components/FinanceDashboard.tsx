// Net worth stat tiles + asset-allocation bar, from the deterministic /snapshot API.
// Colors: categorical slots in fixed order; every segment is direct-labeled in the
// legend rows (text ink), with 2px surface gaps between segments.
import type { Snapshot } from "@/lib/types";
import RiskCard from "./RiskCard";

const SLOTS = ["var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)", "var(--series-5)"];

export function formatINR(n: number): string {
  if (n >= 1e7) return `₹${(n / 1e7).toFixed(2)}Cr`;
  if (n >= 1e5) return `₹${(n / 1e5).toFixed(2)}L`;
  return `₹${n.toLocaleString("en-IN")}`;
}

function StatTile({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="card p-4">
      <p className="text-xs" style={{ color: "var(--ink-muted)" }}>{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
      {sub && <p className="mt-0.5 text-xs" style={{ color: "var(--ink-2)" }}>{sub}</p>}
    </div>
  );
}

export default function FinanceDashboard({ snapshot }: { snapshot: Snapshot }) {
  const entries = Object.entries(snapshot.assets).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const totalAssets = entries.reduce((s, [, v]) => s + v, 0);
  const liabilities = Object.values(snapshot.liabilities).reduce((s, v) => s + v, 0);

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        <StatTile label="Net worth" value={formatINR(snapshot.total_net_worth)} />
        <StatTile
          label="Credit score"
          value={snapshot.credit_score != null ? String(snapshot.credit_score) : "—"}
          sub={snapshot.credit_score == null ? "not connected" : undefined}
        />
        <StatTile
          label="Liabilities"
          value={liabilities > 0 ? formatINR(liabilities) : "₹0"}
          sub={liabilities === 0 ? "none recorded" : undefined}
        />
      </div>

      {entries.length > 0 && (
        <div className="card p-4">
          <h3 className="mb-3 text-sm font-semibold">Asset allocation</h3>
          <div
            className="flex h-4 w-full overflow-hidden rounded"
            role="img"
            aria-label={`Asset allocation: ${entries.map(([k, v]) => `${k} ${formatINR(v)}`).join(", ")}`}
          >
            {entries.map(([name, value], i) => (
              <div
                key={name}
                title={`${name}: ${formatINR(value)}`}
                style={{
                  width: `${(value / totalAssets) * 100}%`,
                  background: SLOTS[i],
                  borderRight: i < entries.length - 1 ? "2px solid var(--surface-1)" : undefined,
                }}
              />
            ))}
          </div>
          <ul className="mt-3 space-y-1">
            {entries.map(([name, value], i) => (
              <li key={name} className="flex items-center gap-2 text-xs">
                <span aria-hidden className="inline-block h-2.5 w-2.5 rounded-sm" style={{ background: SLOTS[i] }} />
                <span>{name}</span>
                <span className="ml-auto font-medium" style={{ color: "var(--ink-2)" }}>
                  {formatINR(value)} · {((value / totalAssets) * 100).toFixed(1)}%
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid gap-2 sm:grid-cols-2">
        {snapshot.risk_signals.map((s) => (
          <RiskCard key={s.name} signal={s} />
        ))}
      </div>
    </div>
  );
}
