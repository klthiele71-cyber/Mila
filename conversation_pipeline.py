from dataclasses import dataclass
@dataclass(frozen=True)
class ConversationResult:
    request_id: str; response: str; blocked: bool=False
class ConversationPipeline:
    def __init__(self, router): self.router=router
    def handle(self, request_id, text):
        if not text or not text.strip(): return ConversationResult(request_id,"",True)
        provider=self.router.choose()
        if not provider: return ConversationResult(request_id,"",True)
        return ConversationResult(request_id,f"prepared:{provider}:{text}")
