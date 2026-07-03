from pydantic import BaseModel


class ChatState(BaseModel):
    conversation_id: str | None = None
    phone_number: str | None = None
    message: str | None = None
    intent: str | None = None
    response: str | None = None
