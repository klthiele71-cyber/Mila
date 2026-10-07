"""Controlled execution layer for staged Mila changes.

This layer can apply only explicitly staged, non-sensitive changes.
Security components remain protected at the execution boundary.
"""
from dataclasses import dataclass, field
from pathlib import Path

from integration_manager import IntegrationDecision, IntegrationRequest
from rollback import RollbackManager, RollbackRecord
from audit_log import AuditLog


@dataclass(frozen=True)
class ExecutionRequest:
    integration: IntegrationRequest
    decision: IntegrationDecision
    change_paths: list[str]
    change_contents: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionResult:
    executed: bool
    changed_paths: list[str] = field(default_factory=list)
    blocked_paths: list[str] = field(default_factory=list)
    reason: str = ""
    rollback_id: str = ""


class MilaExecutionEngine:
    """Applies only safe, already-approved integration decisions.

    The engine does not decide whether a change is safe. It requires an
    allowed decision from the Integration Manager and independently applies
    a protected-path deny list as a final technical boundary.
    """

    PROTECTED_PATHS = {
        "security.py",
        "security.py:",
        "mila_core.py:security",
        "security_gate",
        "security",
        "SECURITY.md",
        "MODEL_ADAPTER_RULES.md",
        "DEVELOPMENT_AGENT_RULES.md",
    }

    def __init__(self, root: str | Path, audit_log: AuditLog | None = None):
        self.root = Path(root).resolve()
        self.rollback = RollbackManager(self.root)
        self.audit = audit_log or AuditLog()

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        if not request.decision.allowed:
            self.audit.append("EXECUTION_BLOCKED", "BLOCKED", "execution_engine", change_id=request.integration.change_id, details={"reason": "integration decision is not allowed"})
            return ExecutionResult(
                executed=False,
                reason="BLOCK: integration decision is not allowed",
            )

        blocked = [
            p for p in request.change_paths
            if self._is_protected(p) or self._escapes_root(p)
        ]
        if blocked:
            self.audit.append("EXECUTION_BLOCKED", "BLOCKED", "execution_engine", change_id=request.integration.change_id, details={"blocked_paths": blocked})
            return ExecutionResult(
                executed=False,
                blocked_paths=blocked,
                reason="BLOCK: protected or out-of-root path",
            )

        for rel_path in request.change_paths:
            if rel_path not in request.change_contents:
                self.audit.append("EXECUTION_BLOCKED", "BLOCKED", "execution_engine", change_id=request.integration.change_id, details={"reason": f"missing content for {rel_path}"})
                return ExecutionResult(
                    executed=False,
                    reason=f"BLOCK: missing content for {rel_path}",
                )

        snapshot = self.rollback.create_snapshot(request.integration.change_id, request.change_paths)
        changed = []
        try:
            for rel_path in request.change_paths:
                target = self.root / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(request.change_contents[rel_path], encoding="utf-8")
                changed.append(rel_path)
        except Exception as exc:
            self.rollback.rollback(snapshot.rollback_id)
            self.audit.append("EXECUTION_FAILED", "ROLLED_BACK", "execution_engine", change_id=request.integration.change_id, details={"rollback_id": snapshot.rollback_id, "error": str(exc)})
            return ExecutionResult(
                executed=False, changed_paths=changed, rollback_id=snapshot.rollback_id,
                reason=f"FAILED: execution error; automatic rollback completed: {exc}",
            )

        self.audit.append("EXECUTION_COMPLETED", "EXECUTED", "execution_engine", change_id=request.integration.change_id, details={"changed_paths": changed, "rollback_id": snapshot.rollback_id})
        return ExecutionResult(
            executed=True, changed_paths=changed, rollback_id=snapshot.rollback_id,
            reason="EXECUTED: safe staged change applied; rollback snapshot retained",
        )

    def _is_protected(self, path: str) -> bool:
        normalized = path.replace("\\", "/").lower()
        return any(
            protected.lower() == normalized
            or normalized.startswith(protected.lower() + "/")
            for protected in self.PROTECTED_PATHS
        )

    def _escapes_root(self, path: str) -> bool:
        try:
            candidate = (self.root / path).resolve()
            candidate.relative_to(self.root)
            return False
        except ValueError:
            return True
