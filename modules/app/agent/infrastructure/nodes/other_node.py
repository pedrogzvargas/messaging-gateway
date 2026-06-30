from app.agent.application import Other


class OtherNode:

    def __init__(self, service: Other):
        self.service = service

    async def __call__(self, state):
        response = await self.service.execute(conversation_id=state.conversation_id)
        return {"response": response}
