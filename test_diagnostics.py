from diagnostics import Diagnostics

def test_record_and_snapshot():
    d=Diagnostics(); d.record('gateway','ok','READY','ready'); assert d.snapshot()[0]['code']=='READY'
def test_invalid_status_rejected():
    try: Diagnostics().record('x','unknown','X','m')
    except ValueError: return
    assert False
def test_sensitive_content_rejected():
    try: Diagnostics().record('x','error','X','api_key=secret')
    except ValueError: return
    assert False
def test_snapshot_has_no_hidden_authority():
    d=Diagnostics(); d.record('x','ok','X','m'); assert 'approval' not in str(d.snapshot()).lower()
def test_authorization_blocked():
    try: Diagnostics().authorize()
    except PermissionError: return
    assert False
