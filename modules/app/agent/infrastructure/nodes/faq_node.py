from app.agent.application import FAQ


class FAQNode:

    def __init__(self, service: FAQ):
        self.service = service

    async def __call__(self, state):
        response = await self.service.execute(question=state.message, conversation_id=state.conversation_id)
        return {"response": response}
