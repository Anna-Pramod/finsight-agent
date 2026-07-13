// A health signal about the person's finances, with plain-language naming.
import type { RiskSignal } from "@/lib/types";
import { RISK_LABELS } from "@/lib/friendly";

const LEVEL: Record<RiskSignal["level"], { color: string; icon: string; label: string }> = {
  low: { color: "var(--status-good)", icon: "●", label: "Looking fine" },
  medium: { color: "var(--status-warning)", icon: "▲", label: "Worth a look" },
  high: { color: "var(--status-critical)", icon: "■", label: "Needs attention" },
};

export default function RiskCard({ signal }: { signal: RiskSignal }) {
  const l = LEVEL[signal.level];
  return (
    <div className="card flex items-start gap-3 p-3">
      <span aria-hidden style={{ color: l.color }}>{l.icon}</span>
      <div className="min-w-0">
        <p className="text-sm font-medium">
          {RISK_LABELS[signal.name] ?? signal.name.replace(/_/g, " ")} · {l.label}
        </p>
        <p className="text-xs leading-relaxed" style={{ color: "var(--ink-2)" }}>
          {signal.evidence}
        </p>
      </div>
    </div>
  );
}
