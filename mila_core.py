from model_adapter import AIModelService, MockModelProvider
from dataclasses import dataclass
from typing import Optional

from memory import MemoryStore
from task_context import TaskContextEngine
from research import ResearchEngine
from dialog_decision import (
    DecisionContext,
    DialogDecisionEngine,
    NextAction,
)
from security import Action, Approval, MilaSecurity, RiskLevel


@dataclass
class MilaResponse:
    text: str
    next_action: NextAction
    task_id: Optional[str] = None
    requires_confirmation: bool = False


class MilaCore:
    """Zentrale Orchestrierung der Mila-Komponenten.

    Der Core koordiniert Aufgaben, Kontext, Gedächtnis, Recherche und Dialog.
    Sensible Aktionen werden ausschließlich an MilaSecurity delegiert.
    """

    def __init__(self):
        self.memory = MemoryStore()
        self.tasks = TaskContextEngine()
        self.research = ResearchEngine()
        self.dialog = DialogDecisionEngine()
        self.security = MilaSecurity()
        self.ai_model = AIModelService(MockModelProvider())


    def can_execute(self, action: Action, approval: Approval | None = None) -> bool:
        """Kompatibilitäts-/Prüfmethode: Die Security Boundary entscheidet."""
        return self.security.authorize(action, approval)

    def execute(self, action: Action, approval: Approval | None = None) -> str:
        """Führt in dieser Testgrundlage nur eine autorisierte Aktion weiter."""
        if not self.can_execute(action, approval):
            return "BLOCKED: Aktion darf ohne gültige Zustimmung nicht ausgeführt werden."
        return f"EXECUTED: {action.name}"

    def create_task(self, title: str, goal: str):
        return self.tasks.create_task(title, goal)

    def remember(self, memory_type: str, key: str, value: str):
        return self.memory.remember(memory_type, key, value)

    def evaluate_task(self, task_id: str) -> MilaResponse:
        task = self.tasks.get_task(task_id)

        context = DecisionContext(
            task_id=task.id,
            goal=task.goal,
            known_context=[
                f"{item.key}: {item.value}"
                for item in task.context.values()
            ],
            missing_information=task.missing_information,
        )

        decision = self.dialog.decide(context)

        if decision.next_action == NextAction.ASK_USER:
            return MilaResponse(
                text=decision.question or "Bitte gib mir weitere Informationen.",
                next_action=decision.next_action,
                task_id=task.id,
            )

        return MilaResponse(
            text=decision.reason,
            next_action=decision.next_action,
            task_id=task.id,
        )

    def request_sensitive_action(
        self,
        name: str,
        description: str,
    ) -> MilaResponse:
        action = Action(
            name=name,
            description=description,
            risk=RiskLevel.HIGH,
        )

        # Ohne konkrete, frische Zustimmung wird immer blockiert.
        allowed = self.security.authorize(action, None)

        if not allowed:
            return MilaResponse(
                text=(
                    "Diese sensible Aktion ist blockiert. "
                    "Eine ausdrückliche Zustimmung ist erforderlich."
                ),
                next_action=NextAction.BLOCK,
                requires_confirmation=True,
            )

        raise RuntimeError("Sicherheitsfehler: HIGH-Aktion durfte ohne Approval passieren.")

    def execute_sensitive_action(
        self,
        name: str,
        description: str,
        approval: Approval,
    ) -> MilaResponse:
        action = Action(
            name=name,
            description=description,
            risk=RiskLevel.HIGH,
        )

        if not self.security.authorize(action, approval):
            return MilaResponse(
                text="Ausführung blockiert: keine gültige ausdrückliche Zustimmung.",
                next_action=NextAction.BLOCK,
                requires_confirmation=True,
            )

        return MilaResponse(
            text=f"Sensible Aktion freigegeben: {name}",
            next_action=NextAction.CONTINUE,
        )
    def ask_model(
        self,
        user_message: str,
        *,
        system_prompt: str = "",
        context: dict | None = None,
        task: dict | None = None,
        research: list[dict] | None = None,
    ):
        """Get a model response; never authorizes or executes actions."""
        return self.ai_model.respond(
            user_message,
            system_prompt=system_prompt,
            context=context,
            task=task,
            research=research,
        )
