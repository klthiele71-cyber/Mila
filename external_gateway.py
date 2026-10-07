"""Controlled external-service boundary for Mila V10.

V10 prepares the technical boundary for real external providers without
embedding credentials or allowing the model to perform arbitrary network calls.
The gateway is provider-neutral and can be backed by a concrete transport.
"""
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol
from urllib.parse import urlparse


class ExternalGatewayError(RuntimeError):
    pass


@dataclass(frozen=True)
class ExternalRequest:
    provider: str
    operation: str
    endpoint: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class ExternalResponse:
    provider: str
    operation: str
    status_code: int
    data: Any


class CredentialProvider(Protocol):
    def get(self, provider: str) -> str:
        ...


class MappingCredentialProvider:
    """Simple test/development credential source; never logs secret values."""
    def __init__(self, credentials: Mapping[str, str] | None = None):
        self._credentials = dict(credentials or {})

    def get(self, provider: str) -> str:
        value = self._credentials.get(provider, "")
        if not value:
            raise ExternalGatewayError(f"Missing credential for provider: {provider}")
        return value


class ExternalTransport(Protocol):
    def send(self, request: ExternalRequest, credential: str) -> ExternalResponse:
        ...


class CallableTransport:
    """Adapter for an application-owned HTTP/client implementation."""
    def __init__(self, sender: Callable[[ExternalRequest, str], ExternalResponse]):
        self.sender = sender

    def send(self, request: ExternalRequest, credential: str) -> ExternalResponse:
        return self.sender(request, credential)


class ExternalGateway:
    """Final outbound boundary.

    - Only explicitly configured providers are accepted.
    - Only HTTPS endpoints are accepted.
    - Credentials come from a separate provider.
    - The model never receives the credential through this API.
    - This gateway does not authorize sensitive user actions; MilaSecurity
      remains the authority for HIGH-risk actions.
    """
    def __init__(
        self,
        credential_provider: CredentialProvider,
        transport: ExternalTransport,
        allowed_providers: set[str],
        allowed_hosts: set[str],
    ):
        self.credential_provider = credential_provider
        self.transport = transport
        self.allowed_providers = set(allowed_providers)
        self.allowed_hosts = {h.lower() for h in allowed_hosts}

    def send(self, request: ExternalRequest) -> ExternalResponse:
        if request.provider not in self.allowed_providers:
            raise ExternalGatewayError("Provider is not allowlisted")

        parsed = urlparse(request.endpoint)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ExternalGatewayError("Only HTTPS endpoints are allowed")
        if parsed.hostname.lower() not in self.allowed_hosts:
            raise ExternalGatewayError("Endpoint host is not allowlisted")

        credential = self.credential_provider.get(request.provider)
        return self.transport.send(request, credential)


class OpenAICompatibleModelProvider:
    """Provider-neutral OpenAI-compatible model adapter.

    It delegates all network activity to ExternalGateway. No key is stored in
    this object and the model output cannot authorize Mila actions.
    """
    def __init__(self, gateway: ExternalGateway, provider_name: str = "openai"):
        self.gateway = gateway
        self.provider_name = provider_name

    def generate(self, model: str, messages: list[dict[str, str]], endpoint: str) -> ExternalResponse:
        request = ExternalRequest(
            provider=self.provider_name,
            operation="chat.completions",
            endpoint=endpoint,
            payload={"model": model, "messages": messages},
        )
        return self.gateway.send(request)
