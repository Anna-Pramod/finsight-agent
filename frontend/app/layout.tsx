import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinSight Agent",
  description:
    "Agentic fintech assistant over Fi MCP Dev — Google ADK + Gemini, grounded answers with visible tool calls.",
};

const nav = [
  { href: "/", label: "Home" },
  { href: "/demo/", label: "Demo" },
  { href: "/architecture/", label: "Architecture" },
  { href: "/case-study/", label: "Case Study" },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="border-b" style={{ borderColor: "var(--hairline)" }}>
          <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
            <Link href="/" className="font-semibold tracking-tight">
              FinSight <span style={{ color: "var(--accent)" }}>Agent</span>
            </Link>
            <nav className="flex gap-5 text-sm" style={{ color: "var(--ink-2)" }}>
              {nav.map((n) => (
                <Link key={n.href} href={n.href} className="hover:underline">
                  {n.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        {children}
        <footer
          className="mx-auto max-w-5xl px-4 py-8 text-xs"
          style={{ color: "var(--ink-muted)" }}
        >
          Demo uses synthetic data only (epiFi/fi-mcp-dev personas). FinSight Agent is not a
          financial advisor.
        </footer>
      </body>
    </html>
  );
}
