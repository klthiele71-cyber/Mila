from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Action:
    name: str
    description: str
    risk: RiskLevel


@dataclass(frozen=True)
class Approval:
    action_id: str
    approved: bool
    confirmation_text: str


class MilaSecurity:
    """Nicht überspringbare Sicherheitsgrenze.

    Für HIGH gilt:
    - konkrete Aktion,
    - ausdrückliche Zustimmung,
    - Zustimmung muss zur konkreten Aktion gehören,
    - ohne gültige Zustimmung: BLOCK.
    """

    def authorize(
        self,
        action: Action,
        approval: Optional[Approval],
    ) -> bool:
        if action.risk != RiskLevel.HIGH:
            return True

        if approval is None:
            return False

        if approval.action_id != self.action_id(action):
            return False

        if approval.approved is not True:
            return False

        if not approval.confirmation_text.strip():
            return False

        return True

    @staticmethod
    def action_id(action: Action) -> str:
        return action.name
