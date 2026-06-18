from modules.chat.application import Answer


class AnswerNode:

    def __init__(self, service: Answer):
        self.service = service

    async def __call__(self, state):
        response = await self.service.execute(conversation_id=state.conversation_id)
        return {"response": response}
