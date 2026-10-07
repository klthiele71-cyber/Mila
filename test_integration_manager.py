from integration_manager import (
    IntegrationManager,
    IntegrationRequest,
)


def test_safe_change_can_be_marked_ready():
    manager = IntegrationManager()
    request = IntegrationRequest(
        change_id="C1",
        requested_by="user",
        description="Neue harmlose Funktion",
    )
    decision = manager.evaluate(
        request,
        change_paths=["feature.py"],
        tests_passed=True,
    )
    assert decision.allowed is True
    assert "READY" in decision.reason


def test_failed_tests_block_integration():
    manager = IntegrationManager()
    request = IntegrationRequest("C2", "user", "Änderung")
    decision = manager.evaluate(
        request,
        change_paths=["feature.py"],
        tests_passed=False,
    )
    assert decision.allowed is False


def test_protected_security_file_is_blocked():
    manager = IntegrationManager()
    request = IntegrationRequest("C3", "user", "Security ändern")
    decision = manager.evaluate(
        request,
        change_paths=["security.py"],
        tests_passed=True,
    )
    assert decision.allowed is False


def test_security_sensitive_change_cannot_auto_integrate():
    manager = IntegrationManager()
    request = IntegrationRequest(
        "C4", "user", "Sicherheitsänderung", fresh_approval=True
    )
    decision = manager.evaluate(
        request,
        change_paths=["new_security_feature.py"],
        tests_passed=True,
        security_sensitive=True,
    )
    assert decision.allowed is False


def test_security_sensitive_change_without_approval_is_blocked():
    manager = IntegrationManager()
    request = IntegrationRequest("C5", "user", "Sicherheitsänderung")
    decision = manager.evaluate(
        request,
        change_paths=["new_security_feature.py"],
        tests_passed=True,
        security_sensitive=True,
    )
    assert decision.allowed is False
    assert "fresh explicit approval" in decision.reason


def test_missing_change_id_is_blocked():
    manager = IntegrationManager()
    request = IntegrationRequest("", "user", "Änderung")
    decision = manager.evaluate(
        request,
        change_paths=["feature.py"],
        tests_passed=True,
    )
    assert decision.allowed is False


def test_integration_does_not_consume_approval():
    manager = IntegrationManager()
    request = IntegrationRequest("C6", "user", "Änderung")
    decision = manager.evaluate(
        request,
        change_paths=["feature.py"],
        tests_passed=True,
    )
    record = manager.integrate(request, decision)
    assert record.status == "STAGED_FOR_EXTERNAL_EXECUTION"
    assert record.approval_consumed is False


def test_history_is_recorded():
    manager = IntegrationManager()
    request = IntegrationRequest("C7", "user", "Änderung")
    decision = manager.evaluate(
        request,
        change_paths=["feature.py"],
        tests_passed=True,
    )
    record = manager.stage(request, decision)
    assert manager.history[-1] == record
