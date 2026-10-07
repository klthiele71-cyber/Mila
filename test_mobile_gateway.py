from mobile_gateway import MobileGateway, MobileRequest

def test_status_is_available():
    r = MobileGateway().handle(MobileRequest("1", "status", {})); assert r.status == "ok"

def test_sensitive_action_is_blocked():
    r = MobileGateway().handle(MobileRequest("2", "execute_sensitive", {})); assert r.status == "blocked"

def test_missing_request_id_is_blocked():
    r = MobileGateway().handle(MobileRequest("", "status", {})); assert r.status == "blocked"
