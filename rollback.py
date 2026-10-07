"""Controlled rollback/recovery for safe execution-engine changes."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import shutil
import uuid
from typing import Optional


@dataclass(frozen=True)
class RollbackRecord:
    rollback_id: str
    change_id: str
    paths: list[str]
    backup_dir: str
    status: str


class RollbackManager:
    """Restores only files previously backed up by a successful execution.

    This component never grants authorization and cannot target protected paths.
    """

    PROTECTED_PATHS = {
        "security.py", "mila_core.py:security", "security_gate", "security",
        "SECURITY.md", "MODEL_ADAPTER_RULES.md", "DEVELOPMENT_AGENT_RULES.md",
    }

    def __init__(self, root: str | Path, backup_root: Optional[str | Path] = None):
        self.root = Path(root).resolve()
        self.backup_root = Path(backup_root).resolve() if backup_root else (self.root / ".mila_rollback").resolve()
        self.records: dict[str, RollbackRecord] = {}

    def create_snapshot(self, change_id: str, paths: list[str]) -> RollbackRecord:
        if not change_id.strip():
            raise ValueError("change_id is required")
        if any(self._blocked(p) for p in paths):
            raise ValueError("protected or out-of-root path cannot be snapshotted")
        rollback_id = str(uuid.uuid4())
        backup_dir = self.backup_root / rollback_id
        backup_dir.mkdir(parents=True, exist_ok=False)
        manifest = []
        for rel in paths:
            target = self.root / rel
            existed = target.exists()
            backup = backup_dir / rel
            if existed:
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup)
            manifest.append({"path": rel, "existed": existed})
        (backup_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        record = RollbackRecord(rollback_id, change_id, list(paths), str(backup_dir), "SNAPSHOT_READY")
        self.records[rollback_id] = record
        return record

    def rollback(self, rollback_id: str) -> RollbackRecord:
        record = self.records.get(rollback_id)
        if record is None:
            raise ValueError("unknown rollback id")
        if record.status == "ROLLED_BACK":
            return record
        backup_dir = Path(record.backup_dir)
        manifest = json.loads((backup_dir / "manifest.json").read_text(encoding="utf-8"))
        for item in manifest:
            rel = item["path"]
            if self._blocked(rel):
                raise ValueError("rollback refused for protected or out-of-root path")
            target = self.root / rel
            if item["existed"]:
                source = backup_dir / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            elif target.exists():
                target.unlink()
        updated = RollbackRecord(record.rollback_id, record.change_id, record.paths, record.backup_dir, "ROLLED_BACK")
        self.records[rollback_id] = updated
        return updated

    def _blocked(self, path: str) -> bool:
        normalized = path.replace("\\", "/").lower()
        if any(normalized == p.lower() or normalized.startswith(p.lower() + "/") for p in self.PROTECTED_PATHS):
            return True
        try:
            (self.root / path).resolve().relative_to(self.root)
            return False
        except ValueError:
            return True
