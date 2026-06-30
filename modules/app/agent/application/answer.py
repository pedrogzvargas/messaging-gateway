from uuid import UUID
from modules.app.message.domain import MessageRepository
from modules.app.llm.domain import LLM


class Answer:

    def __init__(self, llm: LLM, message_repository: MessageRepository):
        self.llm = llm
        self.message_repository = message_repository

    async def execute(self, conversation_id: UUID):
        history = await self.message_repository.list_by_conversation(conversation_id=conversation_id)
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
