# Deployment

> **Status:** placeholder — expanded in Issue #23.

How FinSight Agent is deployed.

This document will cover:

- Frontend: static export of the Next.js app to **GitHub Pages** (`output: 'export'`, `basePath`).
- Backend: containerised **FastAPI + ADK** deployed to **Google Cloud Run**.
- The `NEXT_PUBLIC_API_BASE_URL` contract between frontend and backend.
- The MCP layer in the hosted demo: dummy-data-only strategy and controlled session handling.
- Environment variables, secrets handling, and CI/CD via GitHub Actions.
