from dataclasses import dataclass
@dataclass(frozen=True)
class ReleaseCandidate: version: str; ready: bool; blockers: tuple=()
class ReleaseCandidateGate:
    def evaluate(self, version, test_failures, config_ok, security_ok, integration_ok):
        blockers=[]
        if test_failures: blockers.append("tests")
        if not config_ok: blockers.append("configuration")
        if not security_ok: blockers.append("security")
        if not integration_ok: blockers.append("integration")
        return ReleaseCandidate(version,not blockers,tuple(blockers))
