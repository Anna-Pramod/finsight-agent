// Shared TypeScript types — mirror the backend Pydantic schemas.

export interface Persona {
  name: string;
  scenario: string;
}

export interface ToolCall {
  tool: string;
  ok: boolean;
  duration_ms: number | null;
  data_present: boolean;
  note: string | null;
}

export interface GroundedAnswer {
  observation: string;
  risk: string | null;
  suggested_next_step: string | null;
  assumptions: string[];
}

export interface ChatResponse {
  session_id: string;
  persona: string;
  answer: GroundedAnswer;
  tools_called: ToolCall[];
  missing_data: string[];
  blocked: boolean;
  disclaimer: string;
}

export interface RiskSignal {
  name: string;
  level: "low" | "medium" | "high";
  evidence: string;
}

export interface Snapshot {
  persona: string;
  total_net_worth: number;
  assets: Record<string, number>;
  liabilities: Record<string, number>;
  credit_score: number | null;
  risk_overall: "low" | "medium" | "high";
  risk_signals: RiskSignal[];
  missing_data: string[];
}
