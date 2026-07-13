import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinSight — understand your money",
  description:
    "Ask questions about your money in plain English and get clear, honest answers grounded in your own financial data.",
};

const nav = [
  { href: "/", label: "Home" },
  { href: "/demo/", label: "Open FinSight" },
  { href: "/architecture/", label: "How it works" },
  { href: "/case-study/", label: "About" },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="border-b" style={{ borderColor: "var(--hairline)" }}>
          <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
            <Link href="/" className="text-lg font-semibold tracking-tight">
              Fin<span style={{ color: "var(--accent)" }}>Sight</span>
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
          className="mx-auto max-w-5xl border-t px-4 py-6 text-xs leading-relaxed"
          style={{ color: "var(--ink-muted)", borderColor: "var(--hairline)" }}
        >
          FinSight explains your finances — it is not a financial adviser and never tells you to
          buy, sell, or borrow. This preview runs on realistic sample data; no real accounts are
          connected.
        </footer>
      </body>
    </html>
  );
}
