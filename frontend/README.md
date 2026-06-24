# Frontend — Next.js + TypeScript + Tailwind

The recruiter-facing FinSight Agent demo. Statically exported and served from **GitHub Pages**.
It calls the deployed backend (Cloud Run) via `NEXT_PUBLIC_API_BASE_URL`.

> **Status:** scaffold only (Issue #1). Pages/components are placeholders; built in Issues #15–#20.

## Pages

- `app/page.tsx` — landing / overview
- `app/demo/page.tsx` — the interactive demo (persona selector, chat, dashboard, tool trace)
- `app/architecture/page.tsx` — architecture explainer
- `app/case-study/page.tsx` — portfolio case study

## Components

`PersonaSelector`, `ChatPanel`, `FinanceDashboard`, `ToolTracePanel`, `RiskCard`, `Disclaimer`.

## Local development (later issues)

```sh
npm install
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 npm run dev   # http://localhost:3000
```

## Static export (GitHub Pages — Issue #16)

`next.config.ts` sets `output: "export"`; `npm run build` produces a static site in `out/`.
For a project site, set `basePath`/`assetPrefix` to `/finsight-agent` before building.
