from task_context import TaskContextEngine


def test_task_and_context():
    engine = TaskContextEngine()
    task = engine.create_task("Projekt planen", "Projekt strukturieren")

    engine.add_context(task.id, "prioritaet", "hoch")
    engine.propose_step(task.id, "Anforderungen sammeln")

    current = engine.get_task(task.id)

    assert current.context["prioritaet"].value == "hoch"
    assert current.proposed_steps == ["Anforderungen sammeln"]


def test_missing_information_is_unique():
    engine = TaskContextEngine()
    task = engine.create_task("Recherche", "Informationen finden")

    question = "Welcher Zeitraum?"
    engine.add_missing_information(task.id, question)
    engine.add_missing_information(task.id, question)

    current = engine.get_task(task.id)
    assert current is not None
    assert current.missing_information == [question]


def test_task_can_be_completed():
    engine = TaskContextEngine()
    task = engine.create_task("Test", "Testziel")

    engine.complete_task(task.id)

    assert engine.get_task(task.id).status == "completed"
