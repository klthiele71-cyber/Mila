from mobile_session_integration import MobileSessionIntegration
def test_bind(): assert MobileSessionIntegration({}).bind("s","r")["bound"]
def test_bind_requires_ids():
 try: MobileSessionIntegration({}).bind("","r"); assert False
 except ValueError: pass
