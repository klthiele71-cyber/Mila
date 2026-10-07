class ModelRouter:
    def __init__(self, providers=None): self.providers=list(providers or [])
    def register(self, name):
        if name not in self.providers: self.providers.append(name)
    def choose(self, preferred=None):
        if preferred and preferred in self.providers: return preferred
        return self.providers[0] if self.providers else None
