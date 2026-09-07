from pydantic import BaseModel


class PatchBusinessPrompt(BaseModel):
    description: str
    content: str
