from credential_store import CredentialStore

def test_reference_resolves_without_storage_in_model():
    s=CredentialStore({'KEY':'secret'}); r=s.register('openai','KEY'); assert s.resolve(r)=='secret'; assert 'secret' not in str(s.describe(r))
def test_missing_credential_blocks():
    s=CredentialStore({}); r=s.register('x','MISSING')
    try: s.resolve(r)
    except PermissionError: return
    assert False
def test_registration_requires_names():
    try: CredentialStore().register('','X')
    except ValueError: return
    assert False
def test_describe_is_nonsecret():
    s=CredentialStore({'K':'topsecret'}); r=s.register('x','K'); assert s.describe(r)=={'name':'x','env_var':'K'}
def test_export_blocked():
    try: CredentialStore({'K':'x'}).export()
    except PermissionError: return
    assert False
