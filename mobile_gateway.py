"""V13 mobile-facing command contract, independent of transport."""
from dataclasses import dataclass

@dataclass(frozen=True)
class MobileRequest:
    request_id: str
    action: str
    payload: dict

@dataclass(frozen=True)
class MobileResponse:
    request_id: str
    status: str
    data: dict

class MobileGateway:
    SAFE_ACTIONS = frozenset({"status", "ask", "capabilities"})
    def handle(self, request: MobileRequest) -> MobileResponse:
        if not request.request_id:
            return MobileResponse("", "blocked", {"reason": "missing request id"})
        if request.action not in self.SAFE_ACTIONS:
            return MobileResponse(request.request_id, "blocked", {"reason": "action requires separate authorization"})
        if request.action == "status":
            return MobileResponse(request.request_id, "ok", {"state": "ready"})
        if request.action == "capabilities":
            return MobileResponse(request.request_id, "ok", {"safe_actions": sorted(self.SAFE_ACTIONS)})
        return MobileResponse(request.request_id, "ok", {"accepted": True, "payload": request.payload})
