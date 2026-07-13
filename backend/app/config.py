"""Application settings.

Loads configuration from the environment / a local ``.env`` file (see
``.env.example`` at the repo root) using pydantic-settings. Covers Gemini /
Vertex AI, the Fi MCP Dev connection, backend server options, and CORS.

Implemented in Issue #3.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings sourced from the environment."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ---- Gemini / Vertex AI -------------------------------------------------
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    google_genai_use_vertexai: bool = Field(
        default=False, alias="GOOGLE_GENAI_USE_VERTEXAI"
    )
    google_cloud_project: str = Field(default="", alias="GOOGLE_CLOUD_PROJECT")
    google_cloud_location: str = Field(
        default="us-central1", alias="GOOGLE_CLOUD_LOCATION"
    )
    gemini_model: str = Field(default="gemini-3.1-flash-lite", alias="GEMINI_MODEL")

    # ---- Fi MCP Dev ---------------------------------------------------------
    fi_mcp_mode: str = Field(
        default="local",
        alias="FI_MCP_MODE",
        description="'local' serves upstream test data in-process; 'http' talks to a running fi-mcp-dev server.",
    )
    fi_mcp_base_url: str = Field(
        default="http://localhost:8080", alias="FI_MCP_BASE_URL"
    )
    fi_mcp_stream_path: str = Field(default="/mcp/stream", alias="FI_MCP_STREAM_PATH")
    mcp_session_prefix: str = Field(default="mcp-session-", alias="MCP_SESSION_PREFIX")
    fi_mcp_demo_phone: str = Field(default="2222222222", alias="FI_MCP_DEMO_PHONE")

    # ---- Backend server -----------------------------------------------------
    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    cors_allow_origins: str = Field(
        default="http://localhost:3000", alias="CORS_ALLOW_ORIGINS"
    )

    @property
    def mcp_stream_url(self) -> str:
        """Full URL of the Fi MCP streaming endpoint."""
        return f"{self.fi_mcp_base_url.rstrip('/')}{self.fi_mcp_stream_path}"

    @property
    def cors_origins(self) -> list[str]:
        """CORS origins parsed from the comma-separated env value."""
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]

    @field_validator("mcp_session_prefix")
    @classmethod
    def _prefix_must_be_nonempty(cls, v: str) -> str:
        # Upstream fi-mcp-dev rejects session IDs not prefixed with "mcp-session-".
        if not v:
            raise ValueError("MCP_SESSION_PREFIX must not be empty")
        return v


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (one per process)."""
    return Settings()


__all__ = ["Settings", "get_settings"]
