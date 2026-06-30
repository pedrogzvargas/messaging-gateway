from app.agent.domain import LLM
from langchain_openai import ChatOpenAI


class OpenaiLLM(LLM):

    def __init__(self, client: ChatOpenAI):
        self.client = client

    async def invoke(self, messages: list):
        response = await self.client.ainvoke(messages)
        return response.content
