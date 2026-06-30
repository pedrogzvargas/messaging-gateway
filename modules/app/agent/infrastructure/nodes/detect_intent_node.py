from app.agent.application import DetectIntent


class DetectIntentNode:

    def __init__(self, service: DetectIntent):
        self.service = service

    async def __call__(self, state):
        message = state.message
        intent = await self.service.execute(question=message)

        return {"intent": f"{intent}"}
