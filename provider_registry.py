"""V11 provider registry: explicit, provider-neutral external model selection."""
from dataclasses import dataclass
from typing import Protocol

class Provider(Protocol):
    name: str
    def invoke(self, payload: dict) -> dict: ...

@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str
    enabled: bool = False
    credential_ref: str | None = None

class ProviderRegistry:
    def __init__(self):
        self._configs: dict[str, ProviderConfig] = {}
        self._providers: dict[str, Provider] = {}

    def register(self, config: ProviderConfig, provider: Provider) -> None:
        if not config.name or config.name != getattr(provider, "name", None):
            raise ValueError("provider name mismatch")
        if config.name in self._configs:
            raise ValueError("provider already registered")
        self._configs[config.name] = config
        self._providers[config.name] = provider

    def select(self, name: str) -> Provider:
        cfg = self._configs.get(name)
        if cfg is None or not cfg.enabled:
            raise PermissionError("provider is not enabled")
        return self._providers[name]

    def describe(self, name: str) -> ProviderConfig:
        return self._configs[name]

    def names(self) -> tuple[str, ...]:
        return tuple(self._configs)

class MockProvider:
    name = "mock"
    def invoke(self, payload: dict) -> dict:
        return {"provider": self.name, "echo": payload}
