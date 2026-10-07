from config_validator import Config,ConfigValidator

def test_valid_config(): assert ConfigValidator().validate(Config(('api.example',)))==()
def test_https_required(): assert 'https required' in ConfigValidator().validate(Config(('x',),False))
def test_allowlist_required(): assert 'allowlist required' in ConfigValidator().validate(Config(()))
def test_limits_checked(): assert ConfigValidator().validate(Config(('x',),True,0,121))==('invalid payload limit','invalid timeout')
def test_raise_on_invalid():
    try: ConfigValidator().validate_or_raise(Config((),True,1,1))
    except ValueError: return
    assert False
