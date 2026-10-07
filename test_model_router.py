from model_router import ModelRouter
def test_router_preferred():
 r=ModelRouter(["mock","openai"]); assert r.choose("openai")=="openai"
def test_router_fallback():
 r=ModelRouter(["mock"]); assert r.choose("openai")=="mock"
def test_router_empty(): assert ModelRouter().choose() is None
