from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class SearchRequest:
    query: str
    task_id: str
    context: List[str] = field(default_factory=list)


@dataclass
class Source:
    title: str
    url: str
    snippet: str
    retrieved_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class ResearchResult:
    request: SearchRequest
    sources: List[Source] = field(default_factory=list)
    summary: str = ""
    uncertainties: List[str] = field(default_factory=list)


class ResearchEngine:
    """Plant und strukturiert Recherche.

    Dieses Modul führt absichtlich noch keine echte Websuche aus.
    Eine spätere Web/API-Anbindung kann hier als austauschbarer Provider
    angeschlossen werden.
    """

    def create_request(
        self,
        task_id: str,
        query: str,
        context: List[str] | None = None,
    ) -> SearchRequest:
        return SearchRequest(
            query=query,
            task_id=task_id,
            context=context or [],
        )

    def build_research_questions(
        self,
        request: SearchRequest,
    ) -> List[str]:
        questions = [
            f"Welche verlässlichen Informationen gibt es zu: {request.query}?",
            "Welche Quellen sind aktuell und glaubwürdig?",
            "Gibt es widersprüchliche Angaben oder offene Punkte?",
        ]
        return questions

    def create_result(
        self,
        request: SearchRequest,
        sources: List[Source],
        summary: str,
        uncertainties: List[str] | None = None,
    ) -> ResearchResult:
        return ResearchResult(
            request=request,
            sources=sources,
            summary=summary,
            uncertainties=uncertainties or [],
        )
