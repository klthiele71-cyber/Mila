from dialog_decision import (
    DecisionContext,
    DialogDecisionEngine,
    NextAction,
)


def test_missing_information_requires_question():
    engine = DialogDecisionEngine()
    context = DecisionContext(
        task_id="1",
        goal="Reise planen",
        missing_information=["Welches Budget hast du?"],
    )

    decision = engine.decide(context)

    assert decision.next_action == NextAction.ASK_USER
    assert decision.question == "Welches Budget hast du?"


def test_high_risk_is_blocked_before_execution():
    engine = DialogDecisionEngine()
    context = DecisionContext(
        task_id="1",
        goal="Zahlung durchführen",
        proposed_action="make_payment",
        proposed_risk="high",
    )

    decision = engine.decide(context)

    assert decision.next_action == NextAction.BLOCK


def test_medium_risk_can_be_prepared():
    engine = DialogDecisionEngine()
    context = DecisionContext(
        task_id="1",
        goal="E-Mail vorbereiten",
        proposed_action="send_email",
        proposed_risk="medium",
    )

    decision = engine.decide(context)

    assert decision.next_action == NextAction.PREPARE


def test_research_possible_when_context_is_sufficient():
    engine = DialogDecisionEngine()
    context = DecisionContext(
        task_id="1",
        goal="Passendes Reiseziel finden",
        known_context=["Oktober", "ruhig"],
    )

    assert engine.should_research(context) is True
