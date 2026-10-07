class SystemIntegration:
    def __init__(self, components): self.components=dict(components)
    def readiness(self):
        required={"security","audit","rollback","mobile","gateway"}
        missing=sorted(required-set(self.components))
        return {"ready":not missing,"missing":missing}
