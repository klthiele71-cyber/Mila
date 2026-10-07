"""Central orchestration layer for Mila.

Coordinates existing components without replacing their authority.
Security remains authoritative and development/integration remain staged.
"""
from dataclasses import dataclass, field
from typing import Any

from dialog_decision import DialogDecisionEngine, NextAction
from model_adapter import AIModelService
from development_agent import MilaDevelopmentAgent, DevelopmentRequest
from integration_manager import IntegrationManager
from audit_log import AuditLog


@dataclass(frozen=True)
class OrchestrationInput:
    user_message: str
    context: dict[str, Any] = field(default_factory=dict)
    task: dict[str, Any] = field(default_factory=dict)
    research: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class OrchestrationResult:
    action: str
    response_text: str | None = None
    development_result: Any = None
    integration_ready: bool = False
    blocked_reason: str | None = None


class MilaOrchestrator:
    """Routes work between Mila's existing components.

    It does not grant authority to any component and never executes a
    sensitive action itself.
    """

    def __init__(
        self,
        dialog_engine: DialogDecisionEngine,
        model_service: AIModelService,
        development_agent: MilaDevelopmentAgent,
        integration_manager: IntegrationManager,
        audit_log: AuditLog | None = None,
    ):
        self.dialog = dialog_engine
        self.model = model_service
        self.development = development_agent
        self.integration = integration_manager
        self.audit = audit_log or AuditLog()

    def respond(self, request: OrchestrationInput) -> OrchestrationResult:
        response = self.model.respond(
            request.user_message,
            context=request.context,
            task=request.task,
            research=request.research,
        )
        return OrchestrationResult(
            action="CONTINUE",
            response_text=response.text,
        )

    def prepare_development(
        self,
        request: OrchestrationInput,
    ) -> OrchestrationResult:
        dev = self.development.prepare(
            DevelopmentRequest(
                goal=request.user_message,
                constraints=list(request.context.get("constraints", [])),
            )
        )
        return OrchestrationResult(
            action="PREPARE_DEVELOPMENT",
            development_result=dev,
            integration_ready=self.development.can_integrate(dev),
        )

    def evaluate_integration(
        self,
        *,
        change_id: str,
        requested_by: str,
        description: str,
        change_paths: list[str],
        tests_passed: bool,
        security_sensitive: bool = False,
        fresh_approval: bool = False,
    ) -> OrchestrationResult:
        req = self.integration_request(
            change_id=change_id,
            requested_by=requested_by,
            description=description,
            fresh_approval=fresh_approval,
        )
        decision = self.integration.evaluate(
            req,
            change_paths=change_paths,
            tests_passed=tests_passed,
            security_sensitive=security_sensitive,
        )
        if not decision.allowed:
            self.audit.append("INTEGRATION_BLOCKED", "BLOCKED", "orchestrator", change_id=change_id, details={"reason": decision.reason})
            return OrchestrationResult(
                action="BLOCK",
                blocked_reason=decision.reason,
            )
        self.audit.append("INTEGRATION_READY", "READY", "orchestrator", change_id=change_id, details={"description": description})
        return OrchestrationResult(
            action="INTEGRATION_READY",
            integration_ready=True,
            response_text=decision.reason,
        )

    @staticmethod
    def integration_request(**kwargs):
        from integration_manager import IntegrationRequest
        return IntegrationRequest(**kwargs)
