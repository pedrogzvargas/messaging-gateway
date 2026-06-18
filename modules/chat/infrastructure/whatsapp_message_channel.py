import httpx
from modules.chat.domain import MessageChannel
from modules.shared.environ.domain import Environ


class WhatsappMessageChannel(MessageChannel):

    def __init__(self, environ: Environ):
        self.environ = environ

    async def send_message(self, identifier: str, message: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self.environ.get_str("WA_API_URL")}/v25.0/{self.environ.get_str("WA_PHONE_NUMBER_ID")}/messages",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.environ.get_str("WA_API_TOKEN")}"
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": f"{identifier}",
                    "type": "text",
                    "text": {
                        "body": f"{message}",
                    }
                }
            )
            print(response.json())
            return response.json()
