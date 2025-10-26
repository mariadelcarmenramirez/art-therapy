from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    """A single message in a chat conversation."""
    role: str  # "user" or "assistant"
    content: str

class ConversationHistory(BaseModel):
    """The full history of a conversation."""
    messages: List[ChatMessage]

class StartResponse(BaseModel):
    """The response from starting a new conversation."""
    first_message: str