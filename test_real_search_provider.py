
from real_search_provider import HttpSearchProvider, SearchProviderConfig
from search_provider import SearchQuery


def fake_http_get(url, api_key, timeout):
    assert "Mila" in url
    assert api_key == "TEST_KEY"
    assert timeout == 10
    return {
        "results": [
            {
                "title": "Mila Test",
                "url": "https://example.invalid/mila",
                "snippet": "Testresultat",
                "retrieved_at": "2026-10-07T00:00:00+00:00",
            }
        ]
    }


def test_http_provider_normalizes_result():
    provider = HttpSearchProvider(
        SearchProviderConfig(
            endpoint="https://search.example.invalid/api",
            api_key="TEST_KEY",
            timeout_seconds=10,
        ),
        http_get=fake_http_get,
    )

    results = provider.search(SearchQuery("Mila", "task-1"))

    assert len(results) == 1
    assert results[0].title == "Mila Test"
    assert results[0].url.endswith("/mila")
