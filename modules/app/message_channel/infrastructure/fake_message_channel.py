from modules.app.message_channel.domain import MessageChannel


class FakeMessageChannel(MessageChannel):

    async def send_message(self, identifier: str, message: str):
        return {
          "messaging_product": "whatsapp",
          "contacts": [
            {
              "input": "+16505551234",
              "wa_id": "16505551234"
            }
          ],
          "messages": [
            {
              "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA"
            }
          ]
        }
