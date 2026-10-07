"""V12 outbound request policy: bounded, auditable, provider-independent."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RequestPolicy:
    timeout_seconds: float = 30.0
    max_payload_bytes: int = 256_000
    max_attempts: int = 1

    def validate(self, payload: bytes) -> None:
        if self.timeout_seconds <= 0 or self.max_payload_bytes <= 0 or self.max_attempts < 1:
            raise ValueError("invalid request policy")
        if len(payload) > self.max_payload_bytes:
            raise ValueError("payload exceeds policy limit")

class RequestExecutor:
    def __init__(self, policy: RequestPolicy | None = None):
        self.policy = policy or RequestPolicy()

    def prepare(self, payload: bytes) -> dict:
        self.policy.validate(payload)
        return {"timeout_seconds": self.policy.timeout_seconds,
                "max_attempts": self.policy.max_attempts,
                "payload": payload}
