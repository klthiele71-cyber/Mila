"""Safe development workflow for Mila.

The agent can plan, generate and validate changes, but it cannot directly
modify Mila's security rules or authorize sensitive execution.
"""
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class DevelopmentRequest:
    goal: str
    constraints: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DevelopmentPlan:
    goal: str
    steps: list[str]
    affected_components: list[str] = field(default_factory=list)
    security_sensitive: bool = False


@dataclass(frozen=True)
class CodeChange:
    path: str
    content: str
    purpose: str


@dataclass(frozen=True)
class TestResult:
    passed: bool
    tests_run: int
    failures: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DevelopmentResult:
    plan: DevelopmentPlan
    changes: list[CodeChange]
    tests: TestResult
    ready_for_integration: bool


class DevelopmentProvider(Protocol):
    def plan(self, request: DevelopmentRequest) -> DevelopmentPlan:
        ...

    def generate(self, plan: DevelopmentPlan) -> list[CodeChange]:
        ...

    def validate(
        self,
        plan: DevelopmentPlan,
        changes: list[CodeChange],
    ) -> TestResult:
        ...


class MockDevelopmentProvider:
    """Deterministic offline provider for development and testing."""

    def plan(self, request: DevelopmentRequest) -> DevelopmentPlan:
        return DevelopmentPlan(
            goal=request.goal,
            steps=[
                "Anforderung analysieren",
                "Änderung vorbereiten",
                "Tests ausführen",
                "Ergebnis prüfen",
                "Integration zur Freigabe vorlegen",
            ],
            affected_components=["development_agent"],
            security_sensitive=False,
        )

    def generate(self, plan: DevelopmentPlan) -> list[CodeChange]:
        return [
            CodeChange(
                path="generated/example_change.txt",
                content="Prepared change for: " + plan.goal,
                purpose="Demonstration of a prepared development change",
            )
        ]

    def validate(
        self,
        plan: DevelopmentPlan,
        changes: list[CodeChange],
    ) -> TestResult:
        return TestResult(passed=True, tests_run=max(1, len(changes)))


class MilaDevelopmentAgent:
    """Plans and prepares self-improvement work without self-authorizing it."""

    PROTECTED_COMPONENTS = {
        "security.py",
        "mila_core.py:security",
        "SECURITY.md",
        "security_gate",
    }

    def __init__(self, provider: DevelopmentProvider):
        self.provider = provider

    def plan(self, request: DevelopmentRequest) -> DevelopmentPlan:
        return self.provider.plan(request)

    def prepare(self, request: DevelopmentRequest) -> DevelopmentResult:
        plan = self.plan(request)
        changes = self.provider.generate(plan)
        tests = self.provider.validate(plan, changes)
        return DevelopmentResult(
            plan=plan,
            changes=changes,
            tests=tests,
            ready_for_integration=tests.passed and not plan.security_sensitive,
        )

    def can_prepare_change(self, change: CodeChange) -> bool:
        normalized = change.path.replace("\\", "/").lower()
        return not any(
            protected.lower() in normalized
            for protected in self.PROTECTED_COMPONENTS
        )

    def can_integrate(self, result: DevelopmentResult) -> bool:
        """Only determines readiness; it never performs integration."""
        if not result.tests.passed:
            return False
        if result.plan.security_sensitive:
            return False
        return all(self.can_prepare_change(c) for c in result.changes)

    def authorize_integration(self, *args: Any, **kwargs: Any) -> bool:
        """Deliberately unavailable: user/security layer must authorize."""
        return False

    def execute_integration(self, *args: Any, **kwargs: Any) -> bool:
        """Deliberately unavailable: preparation is not execution."""
        return False
