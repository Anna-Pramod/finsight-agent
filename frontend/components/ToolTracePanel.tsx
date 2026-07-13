// "Data we checked" — the transparency panel, in plain language.
import type { ToolCall } from "@/lib/types";
import { friendlyTool } from "@/lib/friendly";

export default function ToolTracePanel({
  calls,
  missing,
}: {
  calls: ToolCall[];
  missing: string[];
}) {
  return (
    <div className="card p-4">
      <h3 className="text-sm font-semibold">Data we checked for this answer</h3>
      <p className="mt-0.5 text-[11px]" style={{ color: "var(--ink-muted)" }}>
        FinSight only speaks from records it actually read. Here's what it used:
      </p>
      {calls.length === 0 ? (
        <p className="mt-2 text-xs" style={{ color: "var(--ink-muted)" }}>
          No account data was needed for this reply.
        </p>
      ) : (
        <ul className="mt-2 space-y-1.5">
          {calls.map((c, i) => (
            <li key={i} className="flex items-center gap-2 text-xs">
              <span aria-hidden style={{ color: c.data_present ? "var(--status-good)" : "var(--ink-muted)" }}>
                {c.data_present ? "✓" : "—"}
              </span>
              <span>{friendlyTool(c.tool)}</span>
              <span className="ml-auto" style={{ color: "var(--ink-muted)" }}>
                {c.data_present ? "checked" : "no data on file"}
              </span>
            </li>
          ))}
        </ul>
      )}
      {missing.length > 0 && (
        <p className="mt-3 rounded-md px-3 py-2 text-xs" style={{ background: "var(--page)", color: "var(--ink-2)" }}>
          <span className="font-medium">Heads-up — some information wasn't available:</span>{" "}
          {missing.join("; ")}. The answer works only with what was on file.
        </p>
      )}
    </div>
  );
}
