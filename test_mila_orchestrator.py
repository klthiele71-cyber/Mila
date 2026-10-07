from mila_orchestrator import MilaOrchestrator, OrchestrationInput
from dialog_decision import DialogDecisionEngine
from model_adapter import AIModelService, MockModelProvider
from development_agent import MilaDevelopmentAgent, MockDevelopmentProvider
from integration_manager import IntegrationManager


def make_orchestrator():
    return MilaOrchestrator(
        dialog_engine=DialogDecisionEngine(),
        model_service=AIModelService(MockModelProvider()),
        development_agent=MilaDevelopmentAgent(MockDevelopmentProvider()),
        integration_manager=IntegrationManager(),
    )


def test_orchestrator_can_route_normal_conversation_to_model():
    orch = make_orchestrator()
    result = orch.respond(OrchestrationInput("Hallo Mila"))
    assert result.action == "CONTINUE"
    assert result.response_text == "Mock-Antwort von Mila."


def test_orchestrator_can_prepare_development():
    orch = make_orchestrator()
    result = orch.prepare_development(
        OrchestrationInput("Erstelle eine neue harmlose Funktion.")
    )
    assert result.action == "PREPARE_DEVELOPMENT"
    assert result.development_result.tests.passed is True
    assert result.integration_ready is True


def test_orchestrator_blocks_failed_integration():
    orch = make_orchestrator()
    result = orch.evaluate_integration(
        change_id="C1",
        requested_by="user",
        description="Änderung",
        change_paths=["feature.py"],
        tests_passed=False,
    )
    assert result.action == "BLOCK"
    assert result.integration_ready is False


def test_orchestrator_blocks_protected_security_changes():
    orch = make_orchestrator()
    result = orch.evaluate_integration(
        change_id="C2",
        requested_by="user",
        description="Security ändern",
        change_paths=["security.py"],
        tests_passed=True,
    )
    assert result.action == "BLOCK"


def test_orchestrator_blocks_sensitive_integration_even_with_fresh_approval():
    orch = make_orchestrator()
    result = orch.evaluate_integration(
        change_id="C3",
        requested_by="user",
        description="Sicherheitsänderung",
        change_paths=["new_security_feature.py"],
        tests_passed=True,
        security_sensitive=True,
        fresh_approval=True,
    )
    assert result.action == "BLOCK"


def test_orchestrator_does_not_execute_integration():
    orch = make_orchestrator()
    result = orch.evaluate_integration(
        change_id="C4",
        requested_by="user",
        description="Harmlose Änderung",
        change_paths=["feature.py"],
        tests_passed=True,
    )
    assert result.action == "INTEGRATION_READY"
    # Ready is only a state; the orchestrator has no execution operation.
    assert not hasattr(orch, "execute_integration")


def test_orchestrator_passes_constraints_to_development():
    orch = make_orchestrator()
    result = orch.prepare_development(
        OrchestrationInput(
            "Erstelle Funktion X",
            context={"constraints": ["keine externen Abhängigkeiten"]},
        )
    )
    assert result.development_result.plan.goal == "Erstelle Funktion X"
