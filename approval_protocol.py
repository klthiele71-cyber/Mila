from dataclasses import dataclass
import secrets
from datetime import datetime, timezone

@dataclass(frozen=True)
class Approval:
    approval_id:str; action_id:str; created_at:str; consumed:bool=False

class ApprovalProtocol:
    def __init__(self): self._items={}
    def issue(self, action_id, explicit_confirmation):
        if not explicit_confirmation or explicit_confirmation is not True: raise PermissionError('fresh explicit approval required')
        a=Approval(secrets.token_urlsafe(16),action_id,datetime.now(timezone.utc).isoformat()); self._items[a.approval_id]=a; return a
    def consume_once(self, approval_id, action_id):
        a=self._items.get(approval_id)
        if not a or a.consumed or a.action_id!=action_id: return False
        self._items[approval_id]=Approval(a.approval_id,a.action_id,a.created_at,True); return True
    def valid(self, approval_id, action_id):
        a=self._items.get(approval_id); return bool(a and not a.consumed and a.action_id==action_id)
    def reuse(self,*args,**kwargs): return False
