from operations import Operations
from mobile_gateway import MobileGateway
from provider_registry import ProviderRegistry

def test_health_degraded_when_not_configured():
    assert Operations().health().status == "degraded"

def test_health_ok_when_boundaries_exist():
    o = Operations(ProviderRegistry(), MobileGateway()); assert o.readiness() is True

def test_health_does_not_grant_authorization():
    o = Operations(ProviderRegistry(), MobileGateway()); assert not hasattr(o, "authorize")
