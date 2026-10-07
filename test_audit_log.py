import tempfile
from pathlib import Path
from audit_log import AuditLog


def test_append_and_hash_chain():
    log = AuditLog()
    first = log.append("planned", "PLANNED", "development_agent", change_id="c1")
    second = log.append("tested", "TESTED", "test_runner", change_id="c1")
    assert first.previous_hash == ""
    assert second.previous_hash == first.event_hash
    assert log.verify_integrity()


def test_persistence_and_reload():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "audit.jsonl"
        log = AuditLog(str(path))
        log.append("executed", "EXECUTED", "execution_engine", change_id="c2")
        loaded = AuditLog(str(path))
        assert len(loaded.events) == 1
        assert loaded.events[0].change_id == "c2"
        assert loaded.verify_integrity()


def test_approval_is_evidence_not_authorization():
    log = AuditLog()
    event = log.append("approval_observed", "RECORDED", "user", change_id="c3", approval_id="approval-1")
    assert event.approval_id == "approval-1"
    assert not hasattr(log, "authorize")


def test_tampering_is_detected():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "audit.jsonl"
        log = AuditLog(str(path))
        log.append("blocked", "BLOCKED", "security_gate", change_id="c4")
        raw = path.read_text(encoding="utf-8").replace("BLOCKED", "EXECUTED")
        path.write_text(raw, encoding="utf-8")
        try:
            AuditLog(str(path))
            assert False
        except ValueError:
            assert True
