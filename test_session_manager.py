from session_manager import SessionManager

def test_session_opens_and_validates():
    m=SessionManager(); s=m.open('iphone-1'); assert m.validate(s.session_id,'iphone-1')
def test_wrong_device_rejected():
    m=SessionManager(); s=m.open('a'); assert not m.validate(s.session_id,'b')
def test_revoke_blocks():
    m=SessionManager(); s=m.open('a'); m.revoke(s.session_id); assert not m.validate(s.session_id,'a')
def test_empty_device_rejected():
    try: SessionManager().open('')
    except ValueError: return
    assert False
def test_no_authorization_method():
    try: SessionManager().authorize()
    except PermissionError: return
    assert False
