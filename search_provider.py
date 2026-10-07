from dataclasses import dataclass
from typing import List, Protocol
from datetime import datetime, timezone


@dataclass
class SearchQuery:
    query: str
    task_id: str


@dataclass
class SearchHit:
    title: str
    url: str
    snippet: str
    retrieved_at: str


class SearchProvider(Protocol):
    def search(self, request: SearchQuery) -> List[SearchHit]:
        ...


class MockSearchProvider:
    """Test-Provider ohne Internetzugriff.

    Erlaubt uns, die Mila-Architektur zu testen, bevor ein echter
    Suchdienst angeschlossen wird.
    """

    def search(self, request: SearchQuery) -> List[SearchHit]:
        now = datetime.now(timezone.utc).isoformat()
        return [
            SearchHit(
                title=f"Testtreffer für: {request.query}",
                url="https://example.invalid/result",
                snippet="Dies ist ein künstlicher Treffer für Integrationstests.",
                retrieved_at=now,
            )
        ]


class SearchService:
    def __init__(self, provider: SearchProvider):
        self.provider = provider

    def search(self, query: str, task_id: str) -> List[SearchHit]:
        request = SearchQuery(query=query, task_id=task_id)
        return self.provider.search(request)
