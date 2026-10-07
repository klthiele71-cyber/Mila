"""V32: Real HTTPS transport for the OpenAI Responses API.

The transport is inert until explicitly called. It reads no credentials from
files; the gateway supplies the credential at call time.
"""
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from external_gateway import ExternalRequest, ExternalResponse


class OpenAIHttpTransport:
    def __init__(self, timeout: float = 30.0):
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.timeout = timeout

    def send(self, request: ExternalRequest, credential: str) -> ExternalResponse:
        if not credential:
            raise ValueError("credential is required")
        body = json.dumps(dict(request.payload)).encode("utf-8")
        http_request = Request(
            request.endpoint,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {credential}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urlopen(http_request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw) if raw else {}
                return ExternalResponse(request.provider, request.operation, response.status, data)
        except HTTPError as exc:
            raw = exc.read().decode("utf-8") if exc.fp else ""
            try:
                data = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                data = {"error": raw}
            return ExternalResponse(request.provider, request.operation, exc.code, data)
        except URLError as exc:
            raise RuntimeError(f"external connection failed: {exc.reason}") from exc
