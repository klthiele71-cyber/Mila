from dataclasses import dataclass
import secrets

@dataclass(frozen=True)
class Session:
    session_id: str
    device_id: str
    active: bool = True

class SessionManager:
    def __init__(self): self._sessions = {}
    def open(self, device_id):
        if not device_id: raise ValueError('device_id required')
        sid=secrets.token_urlsafe(18); self._sessions[sid]=Session(sid,device_id,True); return self._sessions[sid]
    def validate(self, session_id, device_id):
        s=self._sessions.get(session_id)
        return bool(s and s.active and secrets.compare_digest(s.device_id, device_id))
    def revoke(self, session_id):
        if session_id in self._sessions:
            s=self._sessions[session_id]; self._sessions[session_id]=Session(s.session_id,s.device_id,False)
    def authorize(self, *args, **kwargs):
        raise PermissionError('SessionManager never grants authorization')
