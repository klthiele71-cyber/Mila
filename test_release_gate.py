from release_gate import ReleaseGate

def test_all_requirements_ready(): assert ReleaseGate().evaluate(True,True,True,True,True).ready
def test_failed_tests_block_release(): r=ReleaseGate().evaluate(False,True,True,True,True); assert not r.ready and 'tests' in r.blockers
def test_security_failure_blocks_release(): r=ReleaseGate().evaluate(True,True,False,True,True); assert not r.ready and 'security' in r.blockers
def test_multiple_blockers_reported(): r=ReleaseGate().evaluate(False,False,True,False,True); assert set(r.blockers)=={'tests','configuration','rollback'}
def test_release_gate_cannot_authorize():
    try: ReleaseGate().authorize()
    except PermissionError: return
    assert False
