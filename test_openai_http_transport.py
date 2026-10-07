from external_gateway import ExternalRequest
from openai_http_transport import OpenAIHttpTransport


def test_transport_requires_credential():
    t = OpenAIHttpTransport()
    try:
        t.send(ExternalRequest("openai", "responses.create", "https://api.openai.com/v1/responses", {"x": 1}), "")
        assert False
    except ValueError as exc:
        assert "credential" in str(exc)


def test_transport_rejects_invalid_timeout():
    try:
        OpenAIHttpTransport(0)
        assert False
    except ValueError:
        pass


def test_transport_does_not_execute_during_construction():
    OpenAIHttpTransport()
    assert True
