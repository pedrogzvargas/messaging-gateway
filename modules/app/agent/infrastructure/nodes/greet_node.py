from modules.app.agent.application import Greet


class GreetNode:

    def __init__(self, service: Greet):
        self.service = service

    async def __call__(self, state):

        response = await self.service.execute(
            business_id=state.business_id,
        )
        return {
            "response": response
        }
