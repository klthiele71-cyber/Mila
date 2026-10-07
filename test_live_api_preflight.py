from external_gateway import ExternalGateway, MappingCredentialProvider, CallableTransport
from live_api_preflight import check_openai_preflight
from openai_responses_provider import OpenAIResponsesConfig


def gateway(credentials=None, providers=None):
    return ExternalGateway(
        MappingCredentialProvider(credentials or {}),
        CallableTransport(lambda request, credential: None),
        set(providers or {"openai"}),
        {"api.openai.com"},
    )


def test_missing_credential_blocks_live_ready_state():
    result = check_openai_preflight(gateway(), OpenAIResponsesConfig("test-model"))
    assert not result.ready_for_live_call
    assert result.reason == "credential not configured"


def test_configured_credential_allows_preflight_only():
    result = check_openai_preflight(gateway({"openai": "secret"}), OpenAIResponsesConfig("test-model"))
    assert result.ready_for_live_call
    assert result.credential_available


def test_provider_must_be_allowlisted():
    result = check_openai_preflight(gateway({"other": "secret"}, {"other"}), OpenAIResponsesConfig("test-model"))
    assert not result.ready_for_live_call
    assert result.reason == "provider not allowlisted"
