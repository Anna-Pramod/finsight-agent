// Typed API client for the FinSight Agent backend.
// The backend base URL comes from the environment (Cloud Run URL in production).
import type { ChatResponse, Persona, Snapshot } from "./types";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) throw new Error(`${path} failed: ${res.status}`);
  return res.json();
}

export const getPersonas = () => get<Persona[]>("/personas");
export const getSnapshot = (persona: string) =>
  get<Snapshot>(`/snapshot/${encodeURIComponent(persona)}`);

export async function postChat(
  persona: string,
  question: string,
  sessionId?: string,
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ persona, question, session_id: sessionId ?? null }),
  });
  if (!res.ok) throw new Error(`/chat failed: ${res.status}`);
  return res.json();
}
