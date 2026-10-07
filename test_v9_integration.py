from pathlib import Path
import tempfile

from audit_log import AuditLog
from execution_engine import MilaExecutionEngine, ExecutionRequest
from integration_manager import IntegrationManager, IntegrationRequest


def test_execution_records_completed_event():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        audit = AuditLog(root / "audit.jsonl")
        manager = IntegrationManager()
        req = IntegrationRequest("c-v9", "Klaus", "safe change", False)
        decision = manager.evaluate(req, change_paths=["demo.txt"], tests_passed=True, security_sensitive=False)
        result = MilaExecutionEngine(root, audit).execute(
            ExecutionRequest(req, decision, ["demo.txt"], {"demo.txt": "hello"})
        )
        assert result.executed is True
        assert audit.events[-1].event_type == "EXECUTION_COMPLETED"
        assert audit.verify_integrity() is True


def test_blocked_execution_is_audited():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        audit = AuditLog()
        manager = IntegrationManager()
        req = IntegrationRequest("c-v9-block", "Klaus", "blocked", False)
        decision = manager.evaluate(req, change_paths=["demo.txt"], tests_passed=False, security_sensitive=False)
        result = MilaExecutionEngine(root, audit).execute(
            ExecutionRequest(req, decision, ["demo.txt"], {"demo.txt": "x"})
        )
        assert result.executed is False
        assert audit.events[-1].status == "BLOCKED"


def test_audit_never_authorizes():
    audit = AuditLog()
    audit.append("APPROVAL_EVIDENCE", "RECORDED", "user", change_id="c1", approval_id="a1")
    assert len(audit.events) == 1
    assert audit.events[0].approval_id == "a1"
    # Presence of an audit entry has no authorization API and cannot make a decision allowed.
    assert not hasattr(audit, "authorize")
