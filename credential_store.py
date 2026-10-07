from dataclasses import dataclass
import os

@dataclass(frozen=True)
class CredentialRef:
    name: str
    env_var: str

class CredentialStore:
    def __init__(self, environ=None): self.environ=dict(os.environ if environ is None else environ)
    def register(self,name,env_var):
        if not name or not env_var: raise ValueError('credential name and env var required')
        return CredentialRef(name,env_var)
    def resolve(self, ref):
        value=self.environ.get(ref.env_var)
        if not value: raise PermissionError('credential unavailable')
        return value
    def describe(self, ref): return {'name':ref.name,'env_var':ref.env_var}
    def export(self,*args,**kwargs): raise PermissionError('credentials cannot be exported')
