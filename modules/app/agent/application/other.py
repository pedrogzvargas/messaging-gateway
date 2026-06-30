from uuid import UUID
from modules.app.message.domain import MessageRepository
from modules.app.llm.domain import LLM


class Other:

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

                    El mensaje recibido no contiene una consulta clara ni suficiente información para determinar la intención del usuario.
                    
                    Objetivo:
                    
                    - Solicitar amablemente una aclaración.
                    - Mantener una respuesta breve y profesional.
                    - No asumir lo que el usuario quiso decir.
                    - No inventar información.
                    - No responder preguntas ajenas a Vualdex.
                    
                    Ejemplos:
                    
                    Usuario: ...
                    Respuesta:
                    No estoy seguro de haber entendido tu mensaje. ¿Podrías darme más detalles sobre tu consulta?
                    
                    Usuario: 👍
                    Respuesta:
                    Gracias. Si necesitas información sobre los servicios de Vualdex, estaré encantado de ayudarte.
                    
                    Usuario: ?
                    Respuesta:
                    ¿Podrías indicarme en qué puedo ayudarte respecto a Vualdex?
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
