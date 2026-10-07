"""V31: OpenAI Responses API provider adapter for Mila.

Network access is deliberately injected through ExternalGateway. This module
contains no API key and cannot authorize Mila actions.
"""
from dataclasses import dataclass
from typing import Any

from external_gateway import ExternalGateway, ExternalRequest, ExternalResponse
from model_adapter import ModelMessage, ModelProvider, ModelRequest, ModelResponse


class OpenAIProviderError(RuntimeError):
    pass


@dataclass(frozen=True)
class OpenAIResponsesConfig:
    model: str
    endpoint: str = "https://api.openai.com/v1/responses"
    provider_name: str = "openai"


class OpenAIResponsesProvider(ModelProvider):
    """Concrete Responses API adapter behind Mila's outbound gateway."""

    def __init__(self, gateway: ExternalGateway, config: OpenAIResponsesConfig):
        self.gateway = gateway
        self.config = config

    @staticmethod
    def _input(messages: list[ModelMessage]) -> list[dict[str, Any]]:
        return [{"role": m.role, "content": m.content} for m in messages]

    @staticmethod
    def _extract_text(data: Any) -> str:
        if isinstance(data, dict):
            text = data.get("output_text")
            if isinstance(text, str):
                return text
            # Compatible fallback for normalized test fixtures.
            output = data.get("output", [])
            parts: list[str] = []
            for item in output if isinstance(output, list) else []:
                for content in item.get("content", []) if isinstance(item, dict) else []:
                    if isinstance(content, dict) and isinstance(content.get("text"), str):
                        parts.append(content["text"])
            return "".join(parts)
        raise OpenAIProviderError("Invalid provider response")

    def generate(self, request: ModelRequest) -> ModelResponse:
        payload: dict[str, Any] = {
            "model": self.config.model,
            "input": self._input(request.messages),
        }
        if request.system_prompt:
            payload["instructions"] = request.system_prompt

        external = ExternalRequest(
            provider=self.config.provider_name,
            operation="responses.create",
            endpoint=self.config.endpoint,
            payload=payload,
        )
        response = self.gateway.send(external)
        if response.status_code < 200 or response.status_code >= 300:
            raise OpenAIProviderError(f"OpenAI request failed: HTTP {response.status_code}")
        return ModelResponse(text=self._extract_text(response.data), raw=response.data)
