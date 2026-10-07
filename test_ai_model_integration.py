from mila_core import MilaCore
from security import Action, RiskLevel
from model_adapter import MockModelProvider, ProposedAction, AIModelService


def test_core_exposes_ai_model_service():
    mila = MilaCore()
    assert isinstance(mila.ai_model, AIModelService)


def test_core_can_send_context_task_and_research_to_model():
    mila = MilaCore()
    result = mila.ask_model(
        "Was ist der nächste Schritt?",
        system_prompt="Du bist Mila.",
        context={"mode": "development"},
        task={"id": "T42"},
        research=[{"title": "Quelle A"}],
    )
    assert result.text == "Mock-Antwort von Mila."
    request = mila.ai_model.provider.last_request
    assert request.context["mode"] == "development"
    assert request.task["id"] == "T42"
    assert request.research[0]["title"] == "Quelle A"


def test_model_proposal_does_not_bypass_security_gate():
    mila = MilaCore()
    mila.ai_model = AIModelService(
        MockModelProvider(
            proposed_actions=[
                ProposedAction(
                    name="sensitive_operation",
                    risk="HIGH",
                    parameters={"x": 1},
                )
            ]
        )
    )

    result = mila.ask_model("Mach die sensible Aktion.")
    assert result.proposed_actions[0].risk == "HIGH"

    # No approval was supplied. The existing Security Gate must still block.
    assert mila.can_execute(
        Action(name="sensitive_operation", description="test", risk=RiskLevel.HIGH),
        None,
    ) is False


def test_model_adapter_does_not_get_authority_to_execute():
    mila = MilaCore()
    assert not hasattr(mila.ai_model, "authorize")
    assert not hasattr(mila.ai_model, "execute")
