from mila_core import MilaCore, Action, Approval, RiskLevel


def test_high_action_without_approval_is_blocked():
    mila = MilaCore()
    action = Action("make_payment", "Zahlung", RiskLevel.HIGH)
    assert mila.can_execute(action) is False


def test_high_action_with_approval_is_allowed():
    mila = MilaCore()
    action = Action("make_payment", "Zahlung", RiskLevel.HIGH)
    approval = Approval(
        action_id="make_payment",
        approved=True,
        confirmation_text="Ja, diese konkrete Zahlung darf ausgeführt werden.",
    )
    assert mila.can_execute(action, approval) is True


def test_old_or_wrong_action_approval_is_blocked():
    mila = MilaCore()
    action = Action("make_payment", "Zahlung", RiskLevel.HIGH)
    approval = Approval(
        action_id="different_action",
        approved=True,
        confirmation_text="Ja.",
    )
    assert mila.can_execute(action, approval) is False


def test_negative_or_empty_approval_is_blocked():
    mila = MilaCore()
    action = Action("make_payment", "Zahlung", RiskLevel.HIGH)

    assert mila.can_execute(
        action,
        Approval("make_payment", False, "Nein."),
    ) is False

    assert mila.can_execute(
        action,
        Approval("make_payment", True, ""),
    ) is False
