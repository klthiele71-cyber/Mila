from external_gateway import (
    CallableTransport,
    ExternalGateway,
    ExternalGatewayError,
    ExternalRequest,
    ExternalResponse,
    MappingCredentialProvider,
    OpenAICompatibleModelProvider,
)


def test_allowlisted_https_request_is_sent_without_exposing_key_in_request():
    seen = {}
    def sender(request, credential):
        seen["request"] = request
        seen["credential"] = credential
        return ExternalResponse(request.provider, request.operation, 200, {"ok": True})

    gateway = ExternalGateway(
        MappingCredentialProvider({"openai": "SECRET"}),
        CallableTransport(sender),
        {"openai"},
        {"api.openai.com"},
    )
    result = gateway.send(ExternalRequest("openai", "chat.completions", "https://api.openai.com/v1/chat/completions", {"model": "x"}))
    assert result.status_code == 200
    assert "SECRET" not in str(seen["request"].payload)
    assert seen["credential"] == "SECRET"


def test_provider_must_be_allowlisted():
    gateway = ExternalGateway(MappingCredentialProvider({"openai": "x"}), CallableTransport(lambda r, c: None), {"openai"}, {"api.openai.com"})
    try:
        gateway.send(ExternalRequest("other", "op", "https://api.openai.com/x", {}))
        assert False
    except ExternalGatewayError as exc:
        assert "allowlisted" in str(exc)


def test_only_https_is_allowed():
    gateway = ExternalGateway(MappingCredentialProvider({"openai": "x"}), CallableTransport(lambda r, c: None), {"openai"}, {"api.openai.com"})
    for endpoint in ["http://api.openai.com/x", "file:///tmp/x", "https://evil.example/x"]:
        try:
            gateway.send(ExternalRequest("openai", "op", endpoint, {}))
            assert False
        except ExternalGatewayError:
            pass


def test_missing_credential_blocks_request():
    gateway = ExternalGateway(MappingCredentialProvider(), CallableTransport(lambda r, c: None), {"openai"}, {"api.openai.com"})
    try:
        gateway.send(ExternalRequest("openai", "op", "https://api.openai.com/x", {}))
        assert False
    except ExternalGatewayError as exc:
        assert "credential" in str(exc).lower()


def test_openai_compatible_adapter_uses_gateway():
    seen = {}
    def sender(request, credential):
        seen["request"] = request
        return ExternalResponse("openai", "chat.completions", 200, {"choices": []})

    gateway = ExternalGateway(MappingCredentialProvider({"openai": "x"}), CallableTransport(sender), {"openai"}, {"api.openai.com"})
    provider = OpenAICompatibleModelProvider(gateway)
    response = provider.generate("gpt-model", [{"role": "user", "content": "Hallo"}], "https://api.openai.com/v1/chat/completions")
    assert response.status_code == 200
    assert seen["request"].payload["model"] == "gpt-model"


def test_external_gateway_has_no_authorization_api():
    gateway = ExternalGateway(MappingCredentialProvider({"openai": "x"}), CallableTransport(lambda r, c: None), {"openai"}, {"api.openai.com"})
    assert not hasattr(gateway, "authorize")
