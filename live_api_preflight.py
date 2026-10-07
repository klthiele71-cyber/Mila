"""V33: final preflight before the first live OpenAI request."""
from dataclasses import dataclass

from external_gateway import ExternalGateway
from openai_responses_provider import OpenAIResponsesConfig


@dataclass(frozen=True)
class LiveApiPreflight:
    provider: str
    endpoint: str
    model: str
    credential_available: bool
    ready_for_live_call: bool
    reason: str


def check_openai_preflight(gateway: ExternalGateway, config: OpenAIResponsesConfig) -> LiveApiPreflight:
    try:
        credential = gateway.credential_provider.get(config.provider_name)
    except Exception:
        credential = ""
    available = bool(credential)
    if config.provider_name not in gateway.allowed_providers:
        return LiveApiPreflight(config.provider_name, config.endpoint, config.model, available, False, "provider not allowlisted")
    if not config.endpoint.startswith("https://"):
        return LiveApiPreflight(config.provider_name, config.endpoint, config.model, available, False, "endpoint must use HTTPS")
    if not available:
        return LiveApiPreflight(config.provider_name, config.endpoint, config.model, False, False, "credential not configured")
    return LiveApiPreflight(config.provider_name, config.endpoint, config.model, True, True, "ready for explicit live call")
