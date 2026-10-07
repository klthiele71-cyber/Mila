from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    allowed_hosts: tuple
    require_https: bool=True
    max_payload_bytes: int=65536
    timeout_seconds: float=15.0

class ConfigValidator:
    def validate(self,c):
        errors=[]
        if not c.require_https: errors.append('https required')
        if not c.allowed_hosts: errors.append('allowlist required')
        if c.max_payload_bytes<=0 or c.max_payload_bytes>10_000_000: errors.append('invalid payload limit')
        if c.timeout_seconds<=0 or c.timeout_seconds>120: errors.append('invalid timeout')
        return tuple(errors)
    def validate_or_raise(self,c):
        e=self.validate(c)
        if e: raise ValueError('; '.join(e))
        return c
