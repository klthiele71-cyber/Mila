from provider_registry import ProviderConfig, ProviderRegistry, MockProvider

def test_register_and_select_enabled_provider():
    r = ProviderRegistry(); p = MockProvider()
    r.register(ProviderConfig("mock", "https://mock.invalid", True), p)
    assert r.select("mock") is p

def test_disabled_provider_blocked():
    r = ProviderRegistry(); r.register(ProviderConfig("mock", "https://mock.invalid", False), MockProvider())
    try: r.select("mock")
    except PermissionError: return
    assert False

def test_duplicate_provider_blocked():
    r = ProviderRegistry(); p = MockProvider()
    r.register(ProviderConfig("mock", "https://mock.invalid", True), p)
    try: r.register(ProviderConfig("mock", "https://mock.invalid", True), p)
    except ValueError: return
    assert False
