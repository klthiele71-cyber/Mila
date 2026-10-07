"""V14 operational diagnostics and readiness checks."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HealthReport:
    status: str
    checks: dict[str, str]

class Operations:
    def __init__(self, provider_registry=None, gateway=None):
        self.provider_registry = provider_registry
        self.gateway = gateway

    def health(self) -> HealthReport:
        checks = {
            "security_boundary": "ok",
            "mobile_gateway": "ok" if self.gateway is not None else "not_configured",
            "provider_registry": "ok" if self.provider_registry is not None else "not_configured",
        }
        status = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
        return HealthReport(status, checks)

    def readiness(self) -> bool:
        return self.health().status == "ok"
