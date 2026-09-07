from uuid import UUID
from modules.app.faq.domain import FaqRepository
from modules.app.message.domain import MessageRepository
from modules.app.business_prompt.domain import BusinessPromptRepository
from modules.app.llm.domain import LLM


class FAQ:

    def __init__(
        self,
        llm: LLM,
        message_repository: MessageRepository,
        faq_repository: FaqRepository,
        business_prompt_repository: BusinessPromptRepository,
    ):
        self.llm = llm
        self.message_repository = message_repository
        self.faq_repository = faq_repository
        self.business_prompt_repository = business_prompt_repository

    async def execute(self, question: str, conversation_id: UUID, business_id: UUID):
        history = await self.message_repository.list_by_conversation(conversation_id=conversation_id)
        questions = await self.faq_repository.search(question=question)
        business_context = await self.business_prompt_repository.get_by_fields(business_id=business_id, key="main_context")
        context = "\n\n".join(
            [
                f"""
                PREGUNTAS FRECUENTES ENCONTRADAS EN BASE DE DATOS
                
                Pregunta: {question.question}
                Respuesta: {question.answer}
                """
                for question in questions
            ]
        )
        messages = [
            {
                "role": "system",
                "content": business_context.content
            },
            {
                "role": "system",
                "content": context
            }, *(
                {
                    "role": message.role,
                    "content": message.message
                } for message in history[::-1]
            )
        ]
        answer = await self.llm.invoke(messages)
        return answer
