"""Persistent, append-only audit log for Mila project changes.

The audit log documents lifecycle events only. It never grants authorization.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    timestamp: str
    event_type: str
    status: str
    actor: str
    change_id: Optional[str] = None
    task_id: Optional[str] = None
    approval_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    previous_hash: str = ""
    event_hash: str = ""


class AuditLog:
    """Append-only audit trail with JSONL persistence and hash chaining."""

    def __init__(self, path: Optional[str] = None):
        self.path = Path(path) if path else None
        self._events: List[AuditEvent] = []
        if self.path and self.path.exists():
            self._load()

    @property
    def events(self) -> List[AuditEvent]:
        return list(self._events)

    def append(
        self,
        event_type: str,
        status: str,
        actor: str,
        *,
        change_id: Optional[str] = None,
        task_id: Optional[str] = None,
        approval_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:
        previous_hash = self._events[-1].event_hash if self._events else ""
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "event_id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "event_type": event_type,
            "status": status,
            "actor": actor,
            "change_id": change_id,
            "task_id": task_id,
            "approval_id": approval_id,
            "details": details or {},
            "previous_hash": previous_hash,
        }
        event_hash = self._hash_payload(payload)
        event = AuditEvent(**payload, event_hash=event_hash)
        self._events.append(event)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(event), ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def record_change(self, change_id: str, event_type: str, status: str, actor: str, details=None, approval_id=None):
        return self.append(event_type, status, actor, change_id=change_id, approval_id=approval_id, details=details)

    def verify_integrity(self) -> bool:
        previous = ""
        for event in self._events:
            data = asdict(event)
            stored = data.pop("event_hash")
            if data["previous_hash"] != previous or self._hash_payload(data) != stored:
                return False
            previous = stored
        return True

    @staticmethod
    def _hash_payload(payload: Dict[str, Any]) -> str:
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _load(self):
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            data = json.loads(line)
            event = AuditEvent(**data)
            self._events.append(event)
        if not self.verify_integrity():
            raise ValueError("Audit log integrity check failed")
