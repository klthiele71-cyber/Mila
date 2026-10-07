from search_provider import MockSearchProvider, SearchService


def test_search_provider_integrates_with_project():
    service = SearchService(MockSearchProvider())
    results = service.search("Mila Integration", "integration-task")

    assert results
    assert results[0].title == "Testtreffer für: Mila Integration"
    assert results[0].retrieved_at
