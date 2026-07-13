// Shows exactly which MCP tools ran for the last answer — the transparency panel.
import type { ToolCall } from "@/lib/types";

export default function ToolTracePanel({
  calls,
  missing,
}: {
  calls: ToolCall[];
  missing: string[];
}) {
  return (
    <div className="card p-4">
      <h3 className="mb-2 text-sm font-semibold">Tool trace</h3>
      {calls.length === 0 ? (
        <p className="text-xs" style={{ color: "var(--ink-muted)" }}>
          No data tools were called for this answer.
        </p>
      ) : (
        <ul className="space-y-1.5">
          {calls.map((c, i) => (
            <li key={i} className="flex items-center gap-2 text-xs font-mono">
              <span aria-hidden style={{ color: c.data_present ? "var(--status-good)" : "var(--ink-muted)" }}>
                {c.data_present ? "✓" : "∅"}
              </span>
              <span>{c.tool}</span>
              <span className="ml-auto" style={{ color: "var(--ink-muted)" }}>
                {c.duration_ms != null ? `${c.duration_ms} ms` : ""}
                {!c.data_present && " · no data"}
              </span>
            </li>
          ))}
        </ul>
      )}
      {missing.length > 0 && (
        <p className="mt-3 text-xs" style={{ color: "var(--ink-2)" }}>
          <span className="font-medium">Missing data disclosed:</span> {missing.join("; ")}
        </p>
      )}
    </div>
  );
}
