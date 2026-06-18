import pytest
from unittest.mock import AsyncMock
from unittest.mock import Mock
from modules.chat.infrastructure.graph import AIGraph

@pytest.mark.asyncio
async def test_graph_image():
    session = AsyncMock()
    graph = AIGraph(session, llm=Mock(), question_repository=Mock())
    compiled_graph = graph.build_graph()
    _ = compiled_graph.get_graph().draw_mermaid_png(output_file_path="agent.png")
