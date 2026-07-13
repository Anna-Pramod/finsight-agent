"""Audit logger.

Keeps a structured, in-memory audit trail of every chat turn (question, tools
called, missing data, blocked flag) per session, and emits each record as a
structured log line. In-memory is intentional for the demo: the audit trail is
scoped to the running service, like the upstream server's in-memory sessions.

Implemented in Issue #10.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict

from app.schemas.audit import AuditRecord

logger = logging.getLogger("finsight.audit")


class AuditLog:
    """In-memory audit store keyed by session id."""

    def __init__(self, max_per_session: int = 100) -> None:
        self._records: dict[str, list[AuditRecord]] = defaultdict(list)
        self._max = max_per_session

    def record(self, rec: AuditRecord) -> None:
        bucket = self._records[rec.session_id]
        bucket.append(rec)
        del bucket[: max(0, len(bucket) - self._max)]
        logger.info("audit %s", json.dumps(rec.model_dump(), default=str))

    def for_session(self, session_id: str) -> list[AuditRecord]:
        return list(self._records.get(session_id, []))


# Process-wide singleton used by the API layer.
audit_log = AuditLog()

__all__ = ["AuditLog", "audit_log"]
