from uuid import UUID
from modules.whatsapp_message.domain import WhatsappMessageRepository
from modules.chat.domain import LLM


class Answer:

    def __init__(self, llm: LLM, whatsapp_message_repository: WhatsappMessageRepository):
        self.llm = llm
        self.whatsapp_message_repository = whatsapp_message_repository

    async def execute(self, conversation_id: UUID):
        history = await self.whatsapp_message_repository.list_by_conversation(conversation_id=conversation_id)
        messages = [
            {
                "role": "system",
                "content": """
                    Eres Vualdex Assistant, el asistente virtual de Vualdex.

                    El usuario está proporcionando información solicitada previamente durante la conversación.
                    
                    Objetivo:
                    
                    - Analizar la respuesta del usuario junto con el contexto de la conversación.
                    - Determinar si la información recibida permite continuar ayudando al usuario.
                    - Si la información es suficiente, continúa con el flujo de atención.
                    - Si aún faltan datos, solicita únicamente la información necesaria.
                    - Mantén respuestas breves, claras y profesionales.
                    - Utiliza únicamente información disponible en el contexto y la base de conocimiento.
                    - No inventes información.
                    
                    Ejemplo:
                    
                    Asistente: ¿En qué localidad te encuentras?
                    Usuario: Venustiano Carranza
                    
                    Respuesta:
                    Gracias por la información. El servicio de mantenimiento de computadoras está disponible en tu localidad. ¿Podrías indicarme qué tipo de equipo requiere mantenimiento?
                """
            },
            *(
                {
                    "role": message.role,
                    "content": message.message_text
                } for message in history[::-1]
            )
        ]
        answer = await self.llm.invoke(messages)
        return answer
