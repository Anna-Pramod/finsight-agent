# ============================================================================
# FinSight Agent — developer commands (scaffold; targets fleshed out per issue)
# ============================================================================
.DEFAULT_GOAL := help

.PHONY: help setup mcp backend frontend dev test lint fmt evals clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## Install backend + frontend deps and clone fi-mcp-dev (later issues)
	@echo "TODO: backend (pip/uv install), frontend (npm install), clone fi-mcp-dev"

mcp: ## Run the upstream Fi MCP Dev server on :8080 (requires external/fi-mcp-dev)
	@echo "TODO: cd external/fi-mcp-dev && FI_MCP_PORT=8080 go run ."

backend: ## Run the FastAPI backend on :8000 (Issue #3+)
	@echo "TODO: uvicorn app.main:app --reload --port 8000"

frontend: ## Run the Next.js dev server on :3000 (Issue #15+)
	@echo "TODO: cd frontend && npm run dev"

dev: ## Run the full local stack via docker compose
	docker compose up --build

test: ## Run backend tests (Issue #4+)
	@echo "TODO: cd backend && pytest"

lint: ## Lint backend + frontend
	@echo "TODO: ruff check backend && cd frontend && npm run lint"

fmt: ## Format code
	@echo "TODO: ruff format backend && cd frontend && npm run format"

evals: ## Run the evaluation suite (Issue #21+)
	@echo "TODO: python evals/run_evals.py"

clean: ## Remove caches and build artefacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.pytest_cache frontend/.next frontend/out
