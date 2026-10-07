from request_policy import RequestPolicy, RequestExecutor

def test_policy_accepts_small_payload():
    assert RequestExecutor(RequestPolicy(max_payload_bytes=10)).prepare(b"123")["max_attempts"] == 1

def test_policy_rejects_oversized_payload():
    try: RequestExecutor(RequestPolicy(max_payload_bytes=2)).prepare(b"123")
    except ValueError: return
    assert False

def test_invalid_policy_rejected():
    try: RequestPolicy(max_attempts=0).validate(b"")
    except ValueError: return
    assert False
