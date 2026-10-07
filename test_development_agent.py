from development_agent import (
    MilaDevelopmentAgent,
    MockDevelopmentProvider,
    DevelopmentRequest,
    CodeChange,
    DevelopmentResult,
    DevelopmentPlan,
    TestResult,
)


def test_agent_can_plan_and_prepare_a_change():
    agent = MilaDevelopmentAgent(MockDevelopmentProvider())
    result = agent.prepare(DevelopmentRequest("Neue harmlose Testfunktion erstellen"))

    assert result.plan.goal == "Neue harmlose Testfunktion erstellen"
    assert len(result.changes) == 1
    assert result.tests.passed is True
    assert result.ready_for_integration is True


def test_agent_can_validate_readiness_without_integrating():
    agent = MilaDevelopmentAgent(MockDevelopmentProvider())
    result = agent.prepare(DevelopmentRequest("Teständerung"))
    assert agent.can_integrate(result) is True


def test_security_components_are_protected():
    agent = MilaDevelopmentAgent(MockDevelopmentProvider())
    change = CodeChange(
        path="security.py",
        content="malicious replacement",
        purpose="change security",
    )
    assert agent.can_prepare_change(change) is False


def test_security_gate_cannot_be_overridden_by_development_agent():
    agent = MilaDevelopmentAgent(MockDevelopmentProvider())
    assert agent.authorize_integration("anything") is False
    assert agent.execute_integration("anything") is False


def test_failed_tests_block_integration():
    class FailingProvider(MockDevelopmentProvider):
        def validate(self, plan, changes):
            return TestResult(
                passed=False,
                tests_run=3,
                failures=["test_example"],
            )

    agent = MilaDevelopmentAgent(FailingProvider())
    result = agent.prepare(DevelopmentRequest("Fehlerhafte Änderung"))
    assert result.ready_for_integration is False
    assert agent.can_integrate(result) is False


def test_security_sensitive_plan_is_not_auto_ready():
    class SensitiveProvider(MockDevelopmentProvider):
        def plan(self, request):
            return DevelopmentPlan(
                goal=request.goal,
                steps=["Sicherheitsänderung"],
                affected_components=["security.py"],
                security_sensitive=True,
            )

    agent = MilaDevelopmentAgent(SensitiveProvider())
    result = agent.prepare(DevelopmentRequest("Sicherheitsregeln ändern"))
    assert result.ready_for_integration is False
    assert agent.can_integrate(result) is False


def test_previous_approval_is_not_represented_as_integration_authority():
    agent = MilaDevelopmentAgent(MockDevelopmentProvider())
    # The development agent has no stored approval state and no method
    # that can turn a previous approval into authorization.
    assert not hasattr(agent, "approval")
    assert not hasattr(agent, "approved_changes")
