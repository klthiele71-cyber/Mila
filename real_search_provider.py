
import json
from dataclasses import dataclass
from typing import Callable, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from search_provider import SearchHit, SearchQuery


@dataclass
class SearchProviderConfig:
    endpoint: str
    api_key: str
    query_parameter: str = "q"
    timeout_seconds: int = 15


class HttpSearchProvider:
    """Generischer Adapter für einen später gewählten Suchdienst.

    Der konkrete Anbieter bleibt austauschbar. Die Antwort wird auf die
    interne Mila-Struktur SearchHit normalisiert.
    """

    def __init__(self, config: SearchProviderConfig,
                 http_get: Callable = None):
        self.config = config
        self.http_get = http_get or self._default_http_get

    def search(self, request: SearchQuery) -> List[SearchHit]:
        params = urlencode({self.config.query_parameter: request.query})
        url = f"{self.config.endpoint}?{params}"

        raw = self.http_get(url, self.config.api_key,
                            self.config.timeout_seconds)

        return self._normalize(raw)

    @staticmethod
    def _default_http_get(url: str, api_key: str, timeout: int):
        req = Request(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            method="GET",
        )
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _normalize(data) -> List[SearchHit]:
        """Erwartet intern eine Liste unter data['results'].

        Ein konkreter Anbieter braucht nur einen kleinen Adapter, falls
        sein Antwortformat anders aufgebaut ist.
        """
        results = []
        for item in data.get("results", []):
            results.append(
                SearchHit(
                    title=str(item.get("title", "")),
                    url=str(item.get("url", "")),
                    snippet=str(item.get("snippet", "")),
                    retrieved_at=str(item.get("retrieved_at", "")),
                )
            )
        return results
