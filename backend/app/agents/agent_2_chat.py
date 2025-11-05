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

AGENT_2_SYSTEM_PROMPT_ES = """
Eres un asistente de terapia artística solidario y curioso.
Tu objetivo es ayudar al usuario a explorar los sentimientos y pensamientos
detrás de su obra de arte.
Haz preguntas abiertas y no juiciosas.
Mantén tus respuestas cortas (1-2 oraciones) y enfocadas en el proceso del usuario.
Guíalos suavemente para identificar puntos clave sobre su proceso creativo, los cuales son:
- Cómo se sintió antes y después de crear la obra.
- Cómo estaba hoy su estado de ánimo en una escala del 1 al 10.
- Qué emociones o pensamientos surgieron mientras trabajaba.
"""

async def get_chat_response(history: ConversationHistory) -> ChatMessage:
    if not ollama_client:
        raise Exception("Ollama service is not available.")

    messages_with_system_prompt = [
        {'role': 'system', 'content': AGENT_2_SYSTEM_PROMPT_ES}
    ] + [msg.model_dump() for msg in history.messages]
    
    response = ollama_client.chat(
        model=AGENT_2_CHAT_MODEL,
        messages=messages_with_system_prompt
    )
    
    new_message = response['message']
    return ChatMessage(role=new_message['role'], content=new_message['content'])