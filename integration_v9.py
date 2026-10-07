"""Integration helpers for V7 audit logging and V8 rollback into Mila."""
from audit_log import AuditLog

class MilaIntegration:
    """Shared integration boundary for lifecycle observability.

    Audit data is documentary only and never grants authorization.
    """
    def __init__(self, audit_log: AuditLog | None = None):
        self.audit = audit_log or AuditLog()

    def record(self, event_type: str, status: str, actor: str, **kwargs):
        return self.audit.append(event_type, status, actor, **kwargs)
