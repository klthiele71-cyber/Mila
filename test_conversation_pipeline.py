from conversation_pipeline import ConversationPipeline
from model_router import ModelRouter
def test_pipeline(): assert ConversationPipeline(ModelRouter(["mock"])).handle("1","Hallo").response.startswith("prepared:")
def test_pipeline_blocks_empty(): assert ConversationPipeline(ModelRouter(["mock"])).handle("1","").blocked
def test_pipeline_blocks_without_provider(): assert ConversationPipeline(ModelRouter()).handle("1","Hi").blocked
