from provider_health import ProviderHealthChecker
def test_provider_health_ok(): assert ProviderHealthChecker().check("mock").healthy
def test_provider_health_failure(): assert not ProviderHealthChecker().check("x",False,"down").healthy
