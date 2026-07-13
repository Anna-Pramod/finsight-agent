"""Local dummy-data transport.

Serves the exact same persona data as the upstream ``epiFi/fi-mcp-dev`` server,
read directly from its ``test_data_dir/<phone>/<tool>.json`` files, through the
same ``Transport`` interface as the live HTTP transport.

Why this exists: the hosted demo must run as a single Cloud Run service without
a Go sidecar, and local development shouldn't require a Go toolchain. Fidelity
is preserved because the data files ARE the upstream server's data — the Go
server does nothing but return these files for a logged-in session.

The data directory is resolved from (in order): the ``FI_MCP_DATA_DIR`` env
setting, or the default clone location ``external/fi-mcp-dev/test_data_dir``
relative to the repo root.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PersonaDataNotFound(Exception):
    """The phone number has no test data directory."""


def default_data_dir() -> Path:
    # parents: [0]=app/mcp, [1]=app, [2]=backend, [3]=repo root
    backend_dir = Path(__file__).resolve().parents[2]
    repo_root = backend_dir.parent
    candidates = [
        repo_root / "external" / "fi-mcp-dev" / "test_data_dir",
        backend_dir / "data" / "test_data_dir",  # vendored copy inside the container image
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return candidates[0]


class LocalDataTransport:
    """Transport that reads tool responses from the upstream test data files."""

    def __init__(self, phone: str, data_dir: Path | str | None = None) -> None:
        self._dir = Path(data_dir) if data_dir else default_data_dir()
        self._phone = phone
        if not (self._dir / phone).is_dir():
            raise PersonaDataNotFound(
                f"no test data for phone {phone!r} under {self._dir}"
            )

    def call_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        path = self._dir / self._phone / f"{tool}.json"
        if not path.is_file():
            # Mirrors upstream behaviour of a tool with no data for the persona.
            return {"status": "no_data", "message": f"{tool} has no data for this persona"}
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)


__all__ = ["LocalDataTransport", "PersonaDataNotFound", "default_data_dir"]
