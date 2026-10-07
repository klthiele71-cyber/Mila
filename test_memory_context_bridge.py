from memory_context_bridge import MemoryContextBridge
def test_bridge_keeps_allowed_memory(): assert len(MemoryContextBridge().build([{"type":"fact","value":"x"}])["memories"])==1
def test_bridge_filters_unknown(): assert MemoryContextBridge().build([{"type":"secret","value":"x"}])["memories"]==[]
def test_bridge_task(): assert MemoryContextBridge().build([],"t")["task"]=="t"
