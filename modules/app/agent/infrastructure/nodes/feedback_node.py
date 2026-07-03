from app.agent.application import Feedback


class FeedbackNode:

    def __init__(self, service: Feedback):
        self.service = service

    async def __call__(self, state):
        response = await self.service.execute(conversation_id=state.conversation_id)
        return {"response": response}
