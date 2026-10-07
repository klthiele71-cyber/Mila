from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4


class MemoryType:
    FACT = "fact"
    PREFERENCE = "preference"
    CONTEXT = "context"
    DECISION = "decision"
    TASK = "task"


@dataclass
class Memory:
    id: str
    type: str
    key: str
    value: str
    source: str
    confidence: float = 1.0
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class MemoryStore:
    """Kleine, kontrollierbare Gedächtnisschicht für Mila.

    Wichtig: Diese Komponente speichert nur explizit übergebene Informationen.
    Sie entscheidet nicht selbst, was dauerhaft gespeichert werden soll.
    """

    def __init__(self):
        self._memories: Dict[str, Memory] = {}

    def remember(
        self,
        memory_type: str,
        key: str,
        value: str,
        source: str = "user",
        confidence: float = 1.0,
    ) -> Memory:
        memory = Memory(
            id=str(uuid4()),
            type=memory_type,
            key=key,
            value=value,
            source=source,
            confidence=max(0.0, min(1.0, confidence)),
        )
        self._memories[memory.id] = memory
        return memory

    def find(self, key: Optional[str] = None, memory_type: Optional[str] = None) -> List[Memory]:
        result = list(self._memories.values())

        if key is not None:
            result = [m for m in result if m.key == key]

        if memory_type is not None:
            result = [m for m in result if m.type == memory_type]

        return result

    def forget(self, memory_id: str) -> bool:
        return self._memories.pop(memory_id, None) is not None

    def export(self) -> List[dict]:
        return [
            {
                "id": m.id,
                "type": m.type,
                "key": m.key,
                "value": m.value,
                "source": m.source,
                "confidence": m.confidence,
                "created_at": m.created_at,
                "updated_at": m.updated_at,
            }
            for m in self._memories.values()
        ]
