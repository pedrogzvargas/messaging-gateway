import pytest
from unittest.mock import AsyncMock
from unittest.mock import Mock
from modules.app.agent.infrastructure import BusinessGraph

@pytest.mark.asyncio
async def test_graph_image():
    session = AsyncMock()
    graph = BusinessGraph(session, llm=Mock(), faq_repository=Mock())
    compiled_graph = graph.build_graph()
    _ = compiled_graph.get_graph().draw_mermaid_png(output_file_path="agent.png")
