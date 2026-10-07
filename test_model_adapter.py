from model_adapter import (
    AIModelService,
    MockModelProvider,
    ProposedAction,
    ModelRequest,
    ModelResponse,
)


def test_request_contains_user_message_and_context():
    provider = MockModelProvider()
    service = AIModelService(provider)

    response = service.respond(
        "Was ist der nächste Schritt?",
        system_prompt="Du bist Mila.",
        context={"user_name": "Test", "mode": "development"},
        task={"id": "T1", "status": "open"},
        research=[{"title": "Quelle A", "confidence": 0.9}],
    )

    assert response.text == "Mock-Antwort von Mila."
    request = provider.last_request
    assert request is not None
    assert request.system_prompt == "Du bist Mila."
    assert request.messages[0].role == "user"
    assert request.messages[0].content == "Was ist der nächste Schritt?"
    assert request.context["user_name"] == "Test"
    assert request.task["id"] == "T1"
    assert request.research[0]["title"] == "Quelle A"


def test_provider_abstraction_is_replaceable():
    class CustomProvider:
        def generate(self, request):
            return ModelResponse(text=f"Verarbeitet: {request.messages[0].content}")

    service = AIModelService(CustomProvider())
    result = service.respond("Hallo Mila")
    assert result.text == "Verarbeitet: Hallo Mila"


def test_model_can_propose_action_without_authorizing_it():
    action = ProposedAction(
        name="sensitive_operation",
        risk="HIGH",
        parameters={"example": True},
    )
    provider = MockModelProvider(
        response_text="Ich würde diese Aktion vorschlagen.",
        proposed_actions=[action],
    )
    service = AIModelService(provider)

    result = service.respond("Führe die Aktion aus.")
    assert len(result.proposed_actions) == 1
    assert result.proposed_actions[0].risk == "HIGH"
    # The adapter exposes only a proposal; it has no authorization API.
    assert not hasattr(service, "authorize")
    assert not hasattr(provider, "authorize")


def test_empty_optional_inputs_are_safe():
    provider = MockModelProvider()
    service = AIModelService(provider)
    result = service.respond("Hallo")
    request = provider.last_request

    assert result.text
    assert request is not None
    assert request.context == {}
    assert request.task == {}
    assert request.research == []


def test_model_request_is_immutable_dataclass():
    request = ModelRequest(
        system_prompt="x",
        messages=[],
    )
    try:
        request.system_prompt = "y"
        changed = True
    except Exception:
        changed = False
    assert changed is False
