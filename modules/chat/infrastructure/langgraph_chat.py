from langgraph.graph import StateGraph
from modules.chat.domain import Chat
from .state import ChatState


class LangGraphChat(Chat):

    def __init__(self, graph: StateGraph):
        self.graph = graph

    async def process_message(self, user_id: str, message: str):
        initial_state = ChatState()
        initial_state.message = f"{message}"
        initial_state.phone_number = user_id
        result = await self.graph.ainvoke(initial_state)

        return result
