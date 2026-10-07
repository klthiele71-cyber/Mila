from dataclasses import dataclass
@dataclass(frozen=True)
class ReleaseResult:
    ready: bool
    blockers: tuple
class ReleaseGate:
    def evaluate(self, tests_passed, config_valid, security_intact, rollback_ready, audit_ready):
        blockers=[]
        if not tests_passed: blockers.append('tests')
        if not config_valid: blockers.append('configuration')
        if not security_intact: blockers.append('security')
        if not rollback_ready: blockers.append('rollback')
        if not audit_ready: blockers.append('audit')
        return ReleaseResult(not blockers,tuple(blockers))
    def authorize(self,*args,**kwargs): raise PermissionError('ReleaseGate cannot authorize runtime actions')
