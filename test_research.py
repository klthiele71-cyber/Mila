from research import ResearchEngine, Source


def test_research_request_keeps_task_context():
    engine = ResearchEngine()

    request = engine.create_request(
        task_id="task-123",
        query="Reiseziel finden",
        context=["Oktober", "ruhiger Urlaub"],
    )

    assert request.task_id == "task-123"
    assert "Oktober" in request.context


def test_research_questions_include_source_check():
    engine = ResearchEngine()
    request = engine.create_request("task-1", "Testfrage")

    questions = engine.build_research_questions(request)

    assert any("Quellen" in question for question in questions)


def test_result_keeps_sources_and_uncertainties():
    engine = ResearchEngine()
    request = engine.create_request("task-1", "Testfrage")

    result = engine.create_result(
        request,
        [Source("Beispiel", "https://example.invalid", "Test")],
        "Zusammenfassung",
        ["Daten könnten veraltet sein"],
    )

    assert len(result.sources) == 1
    assert result.uncertainties == ["Daten könnten veraltet sein"]
