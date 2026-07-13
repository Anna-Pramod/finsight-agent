// An evidence-based risk signal. Icon + label always accompany the color.
import type { RiskSignal } from "@/lib/types";

const LEVEL: Record<RiskSignal["level"], { color: string; icon: string; label: string }> = {
  low: { color: "var(--status-good)", icon: "●", label: "Low" },
  medium: { color: "var(--status-warning)", icon: "▲", label: "Medium" },
  high: { color: "var(--status-critical)", icon: "■", label: "High" },
};

export default function RiskCard({ signal }: { signal: RiskSignal }) {
  const l = LEVEL[signal.level];
  return (
    <div className="card flex items-start gap-3 p-3">
      <span aria-hidden style={{ color: l.color }}>{l.icon}</span>
      <div className="min-w-0">
        <p className="text-sm font-medium">
          {signal.name.replace(/_/g, " ")} · {l.label} risk
        </p>
        <p className="text-xs" style={{ color: "var(--ink-2)" }}>
          {signal.evidence}
        </p>
      </div>
    </div>
  );
}
