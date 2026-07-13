// Renders the not-a-financial-advisor disclaimer that ships with every answer.
export default function Disclaimer({ text }: { text?: string }) {
  return (
    <p className="mt-2 text-xs" style={{ color: "var(--ink-muted)" }}>
      {text ??
        "FinSight Agent is not a financial advisor. Educational, data-grounded observations over demo data only."}
    </p>
  );
}
