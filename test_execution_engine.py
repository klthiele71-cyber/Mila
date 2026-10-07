from pathlib import Path
from tempfile import TemporaryDirectory

from execution_engine import ExecutionRequest, MilaExecutionEngine
from integration_manager import IntegrationDecision, IntegrationRequest


def allowed_request(path="feature.py", content="hello"):
    return ExecutionRequest(
        integration=IntegrationRequest("E1", "user", "safe change"),
        decision=IntegrationDecision(True, "READY"),
        change_paths=[path],
        change_contents={path: content},
    )


def test_safe_change_is_executed():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        result = engine.execute(allowed_request())
        assert result.executed is True
        assert (Path(d) / "feature.py").read_text() == "hello"


def test_disallowed_decision_blocks_execution():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        request = allowed_request()
        request = ExecutionRequest(
            integration=request.integration,
            decision=IntegrationDecision(False, "BLOCK"),
            change_paths=request.change_paths,
            change_contents=request.change_contents,
        )
        result = engine.execute(request)
        assert result.executed is False
        assert not (Path(d) / "feature.py").exists()


def test_security_file_is_blocked_at_execution_boundary():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        result = engine.execute(allowed_request("security.py", "bad"))
        assert result.executed is False
        assert "security.py" in result.blocked_paths
        assert not (Path(d) / "security.py").exists()


def test_security_subdirectory_is_blocked():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        result = engine.execute(allowed_request("security/private.py", "bad"))
        assert result.executed is False
        assert result.blocked_paths == ["security/private.py"]


def test_path_escape_is_blocked():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        result = engine.execute(allowed_request("../outside.py", "bad"))
        assert result.executed is False
        assert "../outside.py" in result.blocked_paths


def test_missing_content_blocks_before_write():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        request = ExecutionRequest(
            IntegrationRequest("E2", "user", "change"),
            IntegrationDecision(True, "READY"),
            ["feature.py"],
            {},
        )
        result = engine.execute(request)
        assert result.executed is False
        assert not (Path(d) / "feature.py").exists()


def test_multiple_safe_files_can_be_applied():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        request = ExecutionRequest(
            IntegrationRequest("E3", "user", "multi"),
            IntegrationDecision(True, "READY"),
            ["a.py", "nested/b.txt"],
            {"a.py": "A", "nested/b.txt": "B"},
        )
        result = engine.execute(request)
        assert result.executed is True
        assert len(result.changed_paths) == 2
        assert (Path(d) / "a.py").read_text() == "A"
        assert (Path(d) / "nested/b.txt").read_text() == "B"


def test_execution_requires_allowed_decision_not_just_user_context():
    with TemporaryDirectory() as d:
        engine = MilaExecutionEngine(d)
        request = allowed_request()
        blocked = ExecutionRequest(
            request.integration,
            IntegrationDecision(False, "approval missing"),
            request.change_paths,
            request.change_contents,
        )
        assert engine.execute(blocked).executed is False


def test_safe_execution_provides_rollback_id_and_can_recover():
    import tempfile
    from pathlib import Path
    from execution_engine import MilaExecutionEngine, ExecutionRequest
    from integration_manager import IntegrationRequest, IntegrationDecision
    with tempfile.TemporaryDirectory() as d:
        target = Path(d) / "safe.txt"
        target.write_text("before", encoding="utf-8")
        engine = MilaExecutionEngine(d)
        req = ExecutionRequest(
            integration=IntegrationRequest("rollback-1", "agent", "change"),
            decision=IntegrationDecision(True, "READY"),
            change_paths=["safe.txt"],
            change_contents={"safe.txt": "after"},
        )
        result = engine.execute(req)
        assert result.executed is True
        assert result.rollback_id
        engine.rollback.rollback(result.rollback_id)
        assert target.read_text(encoding="utf-8") == "before"
