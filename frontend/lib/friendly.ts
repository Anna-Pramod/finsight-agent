// Plain-language names for technical identifiers, so the UI never leaks jargon.

export const TOOL_LABELS: Record<string, string> = {
  fetch_net_worth: "Net worth summary",
  fetch_credit_report: "Credit report",
  fetch_epf_details: "Retirement fund (EPF)",
  fetch_mf_transactions: "Mutual fund history",
  fetch_bank_transactions: "Bank transactions",
  fetch_stock_transactions: "Stock trades",
};

export const ASSET_LABELS: Record<string, string> = {
  "Mutual Fund": "Mutual funds",
  Epf: "Retirement fund (EPF)",
  "Savings Accounts": "Savings",
  "Fixed Deposit": "Fixed deposits",
  "Indian Securities": "Indian stocks",
  "Us Securities": "US stocks",
  Sgb: "Gold bonds",
  Etf: "ETFs",
};

export const RISK_LABELS: Record<string, string> = {
  leverage: "Debt load",
  credit_score: "Credit health",
};

// Sample profiles, described the way a person would understand them.
export const PROFILE_BLURBS: Record<string, string> = {
  "No Assets": "Just a savings account — nothing else connected yet",
  "Portfolio Heavyweight": "A seasoned investor with nine mutual funds and every account connected",
  "Lean Investor": "Keeps it simple: one mutual fund and steady savings",
  "Multi-Account Juggler": "Three banks, two retirement accounts — a busy financial life",
  "No Credit Score": "Solid finances, but has never taken credit — so no credit score",
  "No Bank Account": "Invests heavily but banks elsewhere — no bank data connected",
  "Debt-Heavy Low Performer": "Carrying expensive debt and struggling investments",
  "SIP Samurai": "Invests a fixed amount every month, without fail",
  "Fixed Income Fanatic": "Prefers safe, predictable returns over market thrills",
  "Precious Metal Believer": "Keeps a big share of savings in gold",
  "Dormant EPF Earner": "Has an old retirement fund quietly sitting idle",
  "Balanced Growth Tracker": "A little of everything, sensibly diversified",
  "Salary Sinkhole": "Good salary coming in, but little of it stays",
  "Starter Saver": "Early in their career, just starting to build savings",
  "Dual Income Dynamo": "Two earners, strong savings, growing fast",
  "Live-for-Today Spender": "Spends freely today, saves little for tomorrow",
};

export function friendlyTool(tool: string): string {
  return TOOL_LABELS[tool] ?? tool.replace(/^fetch_/, "").replace(/_/g, " ");
}

export function friendlyAsset(name: string): string {
  return ASSET_LABELS[name] ?? name;
}
