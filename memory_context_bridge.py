class MemoryContextBridge:
    def build(self, memories, task=None):
        safe=[]
        for m in memories or []:
            if isinstance(m,dict) and m.get("type") in {"fact","preference","context","decision","task"}: safe.append(dict(m))
        return {"task":task,"memories":safe}
