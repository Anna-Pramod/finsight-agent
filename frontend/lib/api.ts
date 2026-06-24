// API client for the FinSight Agent backend. Fully implemented in Issue #15+.
// The backend base URL comes from the environment (Cloud Run URL in production).
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

// TODO(#15): typed fetch helpers for /health, /personas, /chat, /audit.
export {};
