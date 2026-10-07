from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass
class ContextItem:
    key: str
    value: str
    source: str = "user"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class Task:
    id: str
    title: str
    goal: str
    status: str = "open"
    context: Dict[str, ContextItem] = field(default_factory=dict)
    missing_information: List[str] = field(default_factory=list)
    proposed_steps: List[str] = field(default_factory=list)


class TaskContextEngine:
    """Verwaltet Aufgaben und deren Kontext.

    Diese Komponente entscheidet nicht über sensible Aktionen.
    Ausführung bleibt dem separaten Security Gate vorbehalten.
    """

    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def create_task(self, title: str, goal: str) -> Task:
        task = Task(
            id=str(uuid4()),
            title=title,
            goal=goal,
        )
        self.tasks[task.id] = task
        return task

    def add_context(
        self,
        task_id: str,
        key: str,
        value: str,
        source: str = "user",
    ) -> Task:
        task = self._get_task(task_id)
        task.context[key] = ContextItem(
            key=key,
            value=value,
            source=source,
        )
        return task

    def add_missing_information(self, task_id: str, question: str) -> Task:
        task = self._get_task(task_id)
        if question not in task.missing_information:
            task.missing_information.append(question)
        return task

    def propose_step(self, task_id: str, step: str) -> Task:
        task = self._get_task(task_id)
        task.proposed_steps.append(step)
        return task

    def complete_task(self, task_id: str) -> Task:
        task = self._get_task(task_id)
        task.status = "completed"
        return task

    def get_task(self, task_id: str) -> Task:
        return self._get_task(task_id)

    def _get_task(self, task_id: str) -> Task:
        if task_id not in self.tasks:
            raise KeyError(f"Unbekannte Aufgabe: {task_id}")
        return self.tasks[task_id]


if __name__ == "__main__":
    engine = TaskContextEngine()

    task = engine.create_task(
        "Urlaub planen",
        "Eine passende Reise organisieren",
    )

    engine.add_context(task.id, "reisezeit", "Oktober")
    engine.add_context(task.id, "ziel", "noch offen")
    engine.add_missing_information(
        task.id,
        "Welches Budget steht für die Reise zur Verfügung?",
    )
    engine.propose_step(
        task.id,
        "Nach passenden Reisezielen suchen, sobald Budget und Zeitraum geklärt sind.",
    )

    print(task)
