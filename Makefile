# ============================================================================
# FinSight Agent — developer commands (scaffold; targets fleshed out per issue)
# ============================================================================
.DEFAULT_GOAL := help

.PHONY: help setup mcp backend frontend dev test lint fmt evals clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## Install backend + frontend deps and clone fi-mcp-dev
	cd backend && python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
	cd frontend && npm install
	[ -d external/fi-mcp-dev ] || git clone --depth 1 https://github.com/epiFi/fi-mcp-dev.git external/fi-mcp-dev

mcp: ## Run the upstream Fi MCP Dev server on :8080 (requires Go + external/fi-mcp-dev)
	cd external/fi-mcp-dev && FI_MCP_PORT=8080 go run .

backend: ## Run the FastAPI backend on :8000
	cd backend && PYTHONPATH=. .venv/bin/uvicorn app.main:app --reload --port 8000

frontend: ## Run the Next.js dev server on :3000
	cd frontend && npm run dev

dev: ## Run the full local stack via docker compose
	docker compose up --build

test: ## Run backend tests
	cd backend && .venv/bin/python -m pytest -q

lint: ## Lint backend + frontend
	@echo "TODO: ruff check backend && cd frontend && npm run lint"

fmt: ## Format code
	@echo "TODO: ruff format backend && cd frontend && npm run format"

evals: ## Run the evaluation suite (backend must be running on :8000)
	python3 evals/run_evals.py --api-base-url http://localhost:8000

clean: ## Remove caches and build artefacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.pytest_cache frontend/.next frontend/out
