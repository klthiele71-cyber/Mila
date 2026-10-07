from dataclasses import dataclass
@dataclass(frozen=True)
class ProviderHealth:
    provider: str; healthy: bool; reason: str = ""
class ProviderHealthChecker:
    def check(self, provider, healthy=True, reason=""):
        return ProviderHealth(provider, bool(healthy), reason)
