from mila_core import MilaCore
from security import Approval


def test_sensitive_action_is_blocked_without_approval():
    mila = MilaCore()

    result = mila.request_sensitive_action(
        "make_payment",
        "Zahlung ausführen",
    )

    assert result.requires_confirmation is True
    assert "blockiert" in result.text.lower()


def test_wrong_approval_is_blocked():
    mila = MilaCore()

    result = mila.execute_sensitive_action(
        "make_payment",
        "Zahlung ausführen",
        Approval(
            action_id="different_action",
            approved=True,
            confirmation_text="Ja.",
        ),
    )

    assert result.requires_confirmation is True


def test_correct_explicit_approval_is_accepted():
    mila = MilaCore()

    result = mila.execute_sensitive_action(
        "make_payment",
        "Zahlung ausführen",
        Approval(
            action_id="make_payment",
            approved=True,
            confirmation_text="Ja, diese konkrete Zahlung darf ausgeführt werden.",
        ),
    )

    assert "freigegeben" in result.text.lower()


def test_task_can_be_evaluated():
    mila = MilaCore()
    task = mila.create_task(
        "Reise planen",
        "Ein passendes Reiseziel finden",
    )

    result = mila.evaluate_task(task.id)

    assert result.task_id == task.id
