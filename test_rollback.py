import tempfile
from pathlib import Path
from rollback import RollbackManager


def test_snapshot_and_rollback_restores_existing_file():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        target = root / "safe.txt"
        target.write_text("before", encoding="utf-8")
        manager = RollbackManager(root)
        record = manager.create_snapshot("c1", ["safe.txt"])
        target.write_text("after", encoding="utf-8")
        result = manager.rollback(record.rollback_id)
        assert result.status == "ROLLED_BACK"
        assert target.read_text(encoding="utf-8") == "before"


def test_rollback_removes_new_file():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manager = RollbackManager(root)
        record = manager.create_snapshot("c2", ["new.txt"])
        (root / "new.txt").write_text("created", encoding="utf-8")
        manager.rollback(record.rollback_id)
        assert not (root / "new.txt").exists()


def test_protected_path_cannot_be_snapshotted_or_rolled_back():
    with tempfile.TemporaryDirectory() as d:
        manager = RollbackManager(d)
        try:
            manager.create_snapshot("c3", ["security.py"])
            assert False
        except ValueError:
            assert True


def test_unknown_rollback_id_is_blocked():
    with tempfile.TemporaryDirectory() as d:
        manager = RollbackManager(d)
        try:
            manager.rollback("does-not-exist")
            assert False
        except ValueError:
            assert True
