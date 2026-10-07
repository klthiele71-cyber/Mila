from approval_protocol import ApprovalProtocol

def test_only_true_explicit_confirmation_issues():
    p=ApprovalProtocol(); a=p.issue('act-1',True); assert p.valid(a.approval_id,'act-1')
def test_false_confirmation_blocks():
    try: ApprovalProtocol().issue('a',False)
    except PermissionError: return
    assert False
def test_wrong_action_rejected():
    p=ApprovalProtocol(); a=p.issue('a',True); assert not p.valid(a.approval_id,'b')
def test_approval_is_single_use():
    p=ApprovalProtocol(); a=p.issue('a',True); assert p.consume_once(a.approval_id,'a'); assert not p.consume_once(a.approval_id,'a')
def test_no_reuse_shortcut():
    assert ApprovalProtocol().reuse('x','y') is False
