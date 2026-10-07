from system_integration import SystemIntegration
def test_system_ready(): assert SystemIntegration({k:object() for k in ["security","audit","rollback","mobile","gateway"]}).readiness()["ready"]
def test_system_missing(): assert "audit" in SystemIntegration({"security":object()}).readiness()["missing"]
