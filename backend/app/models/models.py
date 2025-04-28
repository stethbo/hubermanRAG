from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str
    user_id: str
    email: str


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatHistory(BaseModel):
    messages: List[Message] = Field(default_factory=list)


class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True


class ChatResponse(BaseModel):
    response: str
    chat_history: List[Message] 