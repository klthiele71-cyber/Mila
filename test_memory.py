from memory import MemoryStore, MemoryType


def test_remember_and_find():
    store = MemoryStore()
    store.remember(MemoryType.PREFERENCE, "communication_style", "natürlich")

    result = store.find(key="communication_style")

    assert len(result) == 1
    assert result[0].value == "natürlich"


def test_memory_type_filter():
    store = MemoryStore()
    store.remember(MemoryType.FACT, "name", "Mila")
    store.remember(MemoryType.PREFERENCE, "tone", "freundlich")

    result = store.find(memory_type=MemoryType.PREFERENCE)

    assert len(result) == 1
    assert result[0].key == "tone"


def test_forget():
    store = MemoryStore()
    memory = store.remember(MemoryType.CONTEXT, "project", "Mila-Projekt")

    assert store.forget(memory.id) is True
    assert store.find(key="project") == []


def test_confidence_is_bounded():
    store = MemoryStore()
    low = store.remember(MemoryType.FACT, "a", "x", confidence=-5)
    high = store.remember(MemoryType.FACT, "b", "y", confidence=5)

    assert low.confidence == 0.0
    assert high.confidence == 1.0
