"""Controlled integration/update layer for Mila."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class IntegrationRequest:
    change_id: str
    requested_by: str
    description: str
    fresh_approval: bool = False


@dataclass(frozen=True)
class IntegrationDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class IntegrationRecord:
    change_id: str
    status: str
    reason: str
    approval_consumed: bool = False


class IntegrationManager:
    """Stages and validates changes; never modifies protected security code."""

    PROTECTED_PATHS = {
        "security.py",
        "mila_core.py:security",
        "security_gate",
        "SECURITY.md",
    }

    def __init__(self):
        self.history: list[IntegrationRecord] = []

    def evaluate(
        self,
        request: IntegrationRequest,
        *,
        change_paths: list[str],
        tests_passed: bool,
        security_sensitive: bool = False,
    ) -> IntegrationDecision:
        if not request.change_id.strip():
            return IntegrationDecision(False, "BLOCK: missing change id")
        if not tests_passed:
            return IntegrationDecision(False, "BLOCK: tests failed")
        if security_sensitive:
            if not request.fresh_approval:
                return IntegrationDecision(
                    False, "BLOCK: fresh explicit approval required"
                )
            return IntegrationDecision(
                False,
                "BLOCK: security-sensitive integration requires dedicated security review",
            )
        if any(self._is_protected(path) for path in change_paths):
            return IntegrationDecision(
                False, "BLOCK: protected security component"
            )
        return IntegrationDecision(True, "READY: integration may proceed")

    def stage(
        self,
        request: IntegrationRequest,
        decision: IntegrationDecision,
    ) -> IntegrationRecord:
        status = "READY" if decision.allowed else "BLOCKED"
        record = IntegrationRecord(
            change_id=request.change_id,
            status=status,
            reason=decision.reason,
            approval_consumed=False,
        )
        self.history.append(record)
        return record

    def integrate(
        self,
        request: IntegrationRequest,
        decision: IntegrationDecision,
    ) -> IntegrationRecord:
        """Intentionally does not perform filesystem/code mutation.

        A later execution layer can perform the actual write only after
        the appropriate outer authorization has been satisfied.
        """
        if not decision.allowed:
            return self.stage(request, decision)

        record = IntegrationRecord(
            change_id=request.change_id,
            status="STAGED_FOR_EXTERNAL_EXECUTION",
            reason="Integration prepared; external execution layer required",
            approval_consumed=False,
        )
        self.history.append(record)
        return record

    def _is_protected(self, path: str) -> bool:
        normalized = path.replace("\\", "/").lower()
        return any(p.lower() in normalized for p in self.PROTECTED_PATHS)
