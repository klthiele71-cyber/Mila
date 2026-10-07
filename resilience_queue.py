from collections import deque
class ResilienceQueue:
    def __init__(self,max_size=10):
        if max_size<1: raise ValueError("max_size")
        self.max_size=max_size; self._q=deque()
    def put(self,item):
        if len(self._q)>=self.max_size: return False
        self._q.append(item); return True
    def get(self): return self._q.popleft() if self._q else None
    def __len__(self): return len(self._q)
