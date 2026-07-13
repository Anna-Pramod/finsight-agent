// "Your money at a glance" — stat tiles + asset mix, from the person's records.
// Colors: categorical slots in fixed order; every segment is direct-labeled in the
// legend rows (text ink), with 2px surface gaps between segments.
import type { Snapshot } from "@/lib/types";
import { friendlyAsset } from "@/lib/friendly";
import RiskCard from "./RiskCard";

const SLOTS = ["var(--series-1)", "var(--series-2)", "var(--series-3)", "var(--series-4)", "var(--series-5)"];

export function formatINR(n: number): string {
  if (n >= 1e7) return `₹${(n / 1e7).toFixed(2)}Cr`;
  if (n >= 1e5) return `₹${(n / 1e5).toFixed(2)}L`;
  return `₹${n.toLocaleString("en-IN")}`;
}

function scoreWord(score: number): string {
  if (score >= 750) return "healthy";
  if (score >= 650) return "fair";
  return "needs care";
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
      <h2 className="text-sm font-semibold">Your money at a glance</h2>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-1 xl:grid-cols-3">
        <StatTile label="What you're worth" value={formatINR(snapshot.total_net_worth)} sub="assets minus debts" />
        <StatTile
          label="Credit score"
          value={snapshot.credit_score != null ? String(snapshot.credit_score) : "—"}
          sub={snapshot.credit_score != null ? scoreWord(snapshot.credit_score) : "no credit history on file"}
        />
        <StatTile
          label="What you owe"
          value={liabilities > 0 ? formatINR(liabilities) : "₹0"}
          sub={liabilities === 0 ? "no debts on file" : "across all loans"}
        />
      </div>

      {entries.length > 0 && (
        <div className="card p-4">
          <h3 className="text-sm font-semibold">Where your money sits</h3>
          <div
            className="mt-3 flex h-4 w-full overflow-hidden rounded"
            role="img"
            aria-label={`Asset mix: ${entries.map(([k, v]) => `${friendlyAsset(k)} ${formatINR(v)}`).join(", ")}`}
          >
            {entries.map(([name, value], i) => (
              <div
                key={name}
                title={`${friendlyAsset(name)}: ${formatINR(value)}`}
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
                <span>{friendlyAsset(name)}</span>
                <span className="ml-auto font-medium" style={{ color: "var(--ink-2)" }}>
                  {formatINR(value)} · {((value / totalAssets) * 100).toFixed(1)}%
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid gap-2">
        {snapshot.risk_signals.map((s) => (
          <RiskCard key={s.name} signal={s} />
        ))}
      </div>
    </div>
  );
}
