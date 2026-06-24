"""FinSight Agent — FastAPI application entrypoint.

Creates the FastAPI app and (in later issues) mounts the API routers
(health, chat, personas, audit), configures CORS, and wires up the
ADK agent + shared MCP session lifecycle.

Status: placeholder (scaffold). Routers and lifecycle wired in Issues #3, #4, #9.
"""

from fastapi import FastAPI

app = FastAPI(
    title="FinSight Agent API",
    version="0.0.1",
    description="Agentic fintech assistant over Fi MCP Dev (Google ADK + Gemini).",
)

# TODO(#4): include health router.
# TODO(#9): include chat router.
# TODO(#8): include personas router.
# TODO(#10): include audit router.
# TODO(#3): configure CORS from settings (CORS_ALLOW_ORIGINS).
