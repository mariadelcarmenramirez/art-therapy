from ..services.ollama_service import ollama_client, AGENT_3_SUMMARY_MODEL
from ..models.schemas import ConversationHistory, ChatMessage

AGENT_3_SYSTEM_PROMPT = """
You are a clinical assistant writing a summary for an art therapist.
The following is a conversation between a client and an AI assistant
about a piece of artwork.

Your task is to synthesize this conversation into a concise summary.
Focus on these key points for the therapist's review:
1.  **Artwork Description:** Briefly describe the artwork based on the user's own words.
2.  **Reported Emotions:** What feelings did the user explicitly mention?
3.  **Key Insights:** What connections or "aha" moments did the user express?
4.  **Potential Topics:** What unresolved topics or strong feelings might
    be important to discuss in the next therapy session?

Format the output clearly using Markdown. Be concise and professional.
"""

async def get_summary_response(history: ConversationHistory) -> ChatMessage:
    if not ollama_client:
        raise Exception("Ollama service is not available.")

    conversation_text = "\n".join(
        [f"{msg.role}: {msg.content}" for msg in history.messages]
    )
    final_prompt = f"Here is the conversation:\n\n{conversation_text}"
    
    messages_for_summary = [
        {'role': 'system', 'content': AGENT_3_SYSTEM_PROMPT},
        {'role': 'user', 'content': final_prompt}
    ]
    
    response = ollama_client.chat(
        model=AGENT_3_SUMMARY_MODEL,
        messages=messages_for_summary
    )
    
    summary_message = response['message']
    return ChatMessage(role=summary_message['role'], content=summary_message['content'])