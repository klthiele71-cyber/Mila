from external_gateway import ExternalGateway, ExternalResponse, MappingCredentialProvider
from model_adapter import ModelMessage, ModelRequest
from openai_responses_provider import OpenAIResponsesConfig, OpenAIResponsesProvider, OpenAIProviderError


class FakeTransport:
    def __init__(self, response):
        self.response = response
        self.last_request = None
        self.last_credential = None

    def send(self, request, credential):
        self.last_request = request
        self.last_credential = credential
        return self.response


def make_provider(data=None, status=200):
    transport = FakeTransport(ExternalResponse("openai", "responses.create", status, data or {"output_text": "Hallo Klaus."}))
    gateway = ExternalGateway(
        MappingCredentialProvider({"openai": "TEST-SECRET"}),
        transport,
        {"openai"},
        {"api.openai.com"},
    )
    provider = OpenAIResponsesProvider(gateway, OpenAIResponsesConfig(model="test-model"))
    return provider, transport


def test_builds_responses_payload_without_exposing_credential():
    provider, transport = make_provider()
    result = provider.generate(ModelRequest(system_prompt="Be helpful", messages=[ModelMessage("user", "Hallo")]))
    assert result.text == "Hallo Klaus."
    assert transport.last_request.operation == "responses.create"
    assert transport.last_request.payload["model"] == "test-model"
    assert transport.last_request.payload["input"][0]["content"] == "Hallo"
    assert "TEST-SECRET" not in repr(transport.last_request.payload)


def test_system_prompt_maps_to_instructions():
    provider, transport = make_provider()
    provider.generate(ModelRequest(system_prompt="SYSTEM", messages=[ModelMessage("user", "x")]))
    assert transport.last_request.payload["instructions"] == "SYSTEM"


def test_extracts_nested_output_text_fixture():
    provider, _ = make_provider({"output": [{"content": [{"text": "Nested"}]}]})
    result = provider.generate(ModelRequest(system_prompt="", messages=[ModelMessage("user", "x")]))
    assert result.text == "Nested"


def test_non_2xx_blocks_response():
    provider, _ = make_provider({"error": "no"}, status=402)
    try:
        provider.generate(ModelRequest(system_prompt="", messages=[ModelMessage("user", "x")]))
        assert False
    except OpenAIProviderError as exc:
        assert "402" in str(exc)


def test_provider_cannot_bypass_gateway_host_allowlist():
    transport = FakeTransport(ExternalResponse("openai", "responses.create", 200, {"output_text": "x"}))
    gateway = ExternalGateway(MappingCredentialProvider({"openai": "secret"}), transport, {"openai"}, {"other.example"})
    provider = OpenAIResponsesProvider(gateway, OpenAIResponsesConfig(model="test-model"))
    try:
        provider.generate(ModelRequest(system_prompt="", messages=[ModelMessage("user", "x")]))
        assert False
    except Exception as exc:
        assert "allowlisted" in str(exc)
