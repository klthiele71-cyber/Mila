from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass(frozen=True)
class DiagnosticEvent:
    component:str; status:str; code:str; message:str

class Diagnostics:
    ALLOWED={'ok','degraded','blocked','error'}
    def __init__(self): self._events=[]
    def record(self,component,status,code,message):
        if status not in self.ALLOWED: raise ValueError('invalid status')
        # Never accept secrets or approval material in diagnostic messages.
        text=str(message)
        if any(x in text.lower() for x in ('api_key','authorization','bearer ')): raise ValueError('sensitive diagnostic content')
        self._events.append(DiagnosticEvent(component,status,code,text)); return self._events[-1]
    def snapshot(self): return [asdict(e) for e in self._events]
    def authorize(self,*args,**kwargs): raise PermissionError('Diagnostics never grants authorization')
