from ..services.ollama_service import ollama_client, AGENT_2_CHAT_MODEL
from ..models.schemas import ConversationHistory, ChatMessage

AGENT_2_SYSTEM_PROMPT = """
You are a supportive and curious art therapy assistant.
Your goal is to help the user explore the feelings and thoughts
behind their artwork.
Ask open-ended, non-judgmental questions.
Keep your responses short (1-2 sentences) and focused on the user's process.
Gently guide them to identify key points about their creative process
(e.g., "That sounds important," or "Tell me more about that feeling.")

**RAG / Fine-Tuning Note:**
This is where your specialization will go.
Your fine-tuned model will know how to guide the conversation
to collect key homework points.
"""

async def get_chat_response(history: ConversationHistory) -> ChatMessage:
    if not ollama_client:
        raise Exception("Ollama service is not available.")

    messages_with_system_prompt = [
        {'role': 'system', 'content': AGENT_2_SYSTEM_PROMPT}
    ] + [msg.model_dump() for msg in history.messages]
    
    response = ollama_client.chat(
        model=AGENT_2_CHAT_MODEL,
        messages=messages_with_system_prompt
    )
    
    new_message = response['message']
    return ChatMessage(role=new_message['role'], content=new_message['content'])