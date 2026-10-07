"""Provider-neutral AI model adapter for Mila.

The model is treated as an untrusted component. It may propose actions,
but it never authorizes or executes sensitive actions.
"""
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ModelMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ProposedAction:
    name: str
    risk: str = "LOW"
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelRequest:
    system_prompt: str
    messages: list[ModelMessage]
    context: dict[str, Any] = field(default_factory=dict)
    task: dict[str, Any] = field(default_factory=dict)
    research: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class ModelResponse:
    text: str
    proposed_actions: list[ProposedAction] = field(default_factory=list)
    raw: Any = None


class ModelProvider(Protocol):
    def generate(self, request: ModelRequest) -> ModelResponse:
        ...


class MockModelProvider:
    """Offline provider used for development and deterministic tests."""

    def __init__(
        self,
        response_text: str = "Mock-Antwort von Mila.",
        proposed_actions: list[ProposedAction] | None = None,
    ):
        self.response_text = response_text
        self.proposed_actions = list(proposed_actions or [])
        self.last_request: ModelRequest | None = None

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.last_request = request
        return ModelResponse(
            text=self.response_text,
            proposed_actions=list(self.proposed_actions),
        )


class AIModelService:
    """Connects Mila's context to a model provider.

    This service prepares model input and returns model output. It does
    not authorize, approve, or execute actions.
    """

    def __init__(self, provider: ModelProvider):
        self.provider = provider

    def build_request(
        self,
        user_message: str,
        *,
        system_prompt: str = "",
        context: dict[str, Any] | None = None,
        task: dict[str, Any] | None = None,
        research: list[dict[str, Any]] | None = None,
    ) -> ModelRequest:
        return ModelRequest(
            system_prompt=system_prompt,
            messages=[ModelMessage(role="user", content=user_message)],
            context=dict(context or {}),
            task=dict(task or {}),
            research=list(research or []),
        )

    def respond(
        self,
        user_message: str,
        *,
        system_prompt: str = "",
        context: dict[str, Any] | None = None,
        task: dict[str, Any] | None = None,
        research: list[dict[str, Any]] | None = None,
    ) -> ModelResponse:
        request = self.build_request(
            user_message,
            system_prompt=system_prompt,
            context=context,
            task=task,
            research=research,
        )
        return self.provider.generate(request)
