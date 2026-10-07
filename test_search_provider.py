from search_provider import MockSearchProvider, SearchService


def test_mock_provider_returns_search_hit():
    service = SearchService(MockSearchProvider())

    results = service.search("Mila Projekt", "task-1")

    assert len(results) == 1
    assert "Mila Projekt" in results[0].title
    assert results[0].url.startswith("https://")


def test_search_keeps_task_identity():
    service = SearchService(MockSearchProvider())

    results = service.search("Test", "task-42")

    assert results[0].retrieved_at
