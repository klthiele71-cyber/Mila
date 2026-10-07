from resilience_queue import ResilienceQueue
def test_queue_capacity():
 q=ResilienceQueue(1); assert q.put("a"); assert not q.put("b")
def test_queue_fifo():
 q=ResilienceQueue(); q.put("a"); q.put("b"); assert q.get()=="a" and q.get()=="b"
def test_queue_empty(): assert ResilienceQueue().get() is None
