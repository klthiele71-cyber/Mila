from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class NextAction(str, Enum):
    CONTINUE = "continue"
    ASK_USER = "ask_user"
    RESEARCH = "research"
    PREPARE = "prepare"
    BLOCK = "block"


@dataclass
class DecisionContext:
    task_id: str
    goal: str
    known_context: List[str] = field(default_factory=list)
    missing_information: List[str] = field(default_factory=list)
    proposed_action: Optional[str] = None
    proposed_risk: Optional[str] = None


@dataclass
class Decision:
    next_action: NextAction
    reason: str
    question: Optional[str] = None


class DialogDecisionEngine:
    """Verbindet Kontext, fehlende Informationen und nächste Schritte.

    Diese Komponente darf keine sensible Aktion selbst freigeben.
    Die eigentliche Berechtigungsprüfung bleibt beim Security Gate.
    """

    def decide(self, context: DecisionContext) -> Decision:
        if context.missing_information:
            return Decision(
                next_action=NextAction.ASK_USER,
                reason="Für die Aufgabe fehlen entscheidende Informationen.",
                question=context.missing_information[0],
            )

        if not context.proposed_action:
            return Decision(
                next_action=NextAction.CONTINUE,
                reason="Kein konkreter externer Aktionsschritt erforderlich.",
            )

        if context.proposed_risk == "high":
            return Decision(
                next_action=NextAction.BLOCK,
                reason=(
                    "Sensible Aktion erkannt. Die Security Boundary muss "
                    "vor jeder Ausführung eine frische Zustimmung einholen."
                ),
            )

        if context.proposed_risk == "medium":
            return Decision(
                next_action=NextAction.PREPARE,
                reason="Aktion darf vorbereitet, aber nicht automatisch ausgeführt werden.",
            )

        return Decision(
            next_action=NextAction.CONTINUE,
            reason="Aktion liegt innerhalb der definierten niedrigen Risikostufe.",
        )

    def should_research(self, context: DecisionContext) -> bool:
        return bool(context.goal.strip()) and not context.missing_information
