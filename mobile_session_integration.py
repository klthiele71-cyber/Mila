class MobileSessionIntegration:
    def __init__(self, sessions): self.sessions=sessions
    def bind(self, session_id, request_id):
        if not session_id or not request_id: raise ValueError("missing identifier")
        return {"session_id":session_id,"request_id":request_id,"bound":True}
