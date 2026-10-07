from release_candidate import ReleaseCandidateGate
def test_release_candidate_ready(): assert ReleaseCandidateGate().evaluate("V30",0,True,True,True).ready
def test_release_candidate_blocks():
 r=ReleaseCandidateGate().evaluate("V30",1,True,True,True); assert not r.ready and "tests" in r.blockers
def test_release_candidate_security_block():
 r=ReleaseCandidateGate().evaluate("V30",0,True,False,True); assert not r.ready and "security" in r.blockers
