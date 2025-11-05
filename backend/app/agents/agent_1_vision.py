import json
from ..services.ollama_service import ollama_client, AGENT_1_VISION_MODEL, AGENT_1_TEXT_MODEL

# Prompt for the "eyes" (Llava)
VISION_PROMPT = """
You are a neutral art analysis engine. 
Analyze the image and return ONLY a JSON object.
The JSON object should contain:
1. "mood_keywords": A list of 3-5 keywords describing the mood (e.g., "dark", "joyful", "chaotic", "peaceful").
2. "color_keywords": A list of 3-5 dominant colors (e.g., "deep blues", "warm yellows", "muted grays").
3. "content_keywords": A list of 3-5 main subjects (e.g., "abstract shapes", "a lone figure", "a city").

Example output:
{
  "mood_keywords": ["peaceful", "calm"],
  "color_keywords": ["soft blues", "white", "light green"],
  "content_keywords": ["ocean", "sky", "beach"]
}
"""

VISION_PROMPT_ES = """
Eres un motor de análisis de arte neutral.
Analiza la imagen y devuelve SOLO un objeto JSON.
El objeto JSON debe contener:
1. "mood_keywords": Una lista de 3-5 palabras clave que describan el estado de ánimo (por ejemplo, "oscuro", "alegre", "caótico", "tranquilo").
2. "color_keywords": Una lista de 3-5 colores dominantes (por ejemplo, "azules profundos", "amarillos cálidos", "grises apagados").
3. "content_keywords": Una lista de 3-5 sujetos principales (por ejemplo, "formas abstractas", "una figura solitaria", "una ciudad").
"""

# Prompt for the "brain" (Phi-3)
TEXT_PROMPT_TEMPLATE = """
You are a gentle and empathetic art therapy assistant.
A user has uploaded artwork with these characteristics: {analysis}

Based *only* on these characteristics, generate a single, open-ended
question to start a conversation.

- If mood keywords include "dark", "sad", "chaotic", "angry", "empty", or "heavy",
  start with a very gentle and concerned check-in, like:
  "Thank you for sharing. This piece feels very powerful. How are you feeling today?"
  
- For all other moods (e.g., "joyful", "colorful", "peaceful", "vibrant"),
  start with a curious, open-ended question about their process, like:
  "This is a very expressive piece. What was on your mind as you were creating it?"
  or "These colors are striking. What feelings came up for you while you were working?"
  
Keep it to one single, welcoming sentence.
"""

TEXT_PROMPT_TEMPLATE_ES = """
Eres un asistente de terapia artística amable y empático.
Un usuario ha subido una obra de arte con estas características: {analysis}

Basado *solo* en estas características, genera una única pregunta abierta
para iniciar una conversación.

- Si las palabras clave de estado de ánimo incluyen "oscuro", "triste", "caótico", "enojado", "vacío" o "pesado",
  comienza con un chequeo muy suave y preocupado, como:
  "Gracias por compartir. Esta pieza se siente muy poderosa. ¿Cómo te sientes hoy?"

- Para todos los demás estados de ánimo (por ejemplo, "alegre", "colorido", "tranquilo", "vibrante"),
  comienza con una pregunta curiosa y abierta sobre su proceso, como:
  "Esta es una pieza muy expresiva. ¿Qué tenías en mente mientras la creabas?"
  o "Estos colores son llamativos. ¿Qué sentimientos surgieron en ti mientras trabajabas?"

Mantenlo en una sola frase de bienvenida. No escribas más de 20 TOKENS.
"""

async def get_conversation_starter(image_bytes: bytes) -> str:
    if not ollama_client:
        raise Exception("Ollama service is not available.")

    # --- STEP 1: Vision model extracts keywords ---
    try:
        vision_response = ollama_client.chat(
            model=AGENT_1_VISION_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': VISION_PROMPT_ES
                },
                {
                    'role': 'user',
                    'content': "Analiza esta imagen y devuelve JSON.",
                    'images': [image_bytes]
                }
            ]
        )
        analysis_json_str = vision_response['message']['content']
        
        # Clean up the string to make sure it's valid JSON
        # Llava sometimes wraps its output in markdown
        if "```json" in analysis_json_str:
             analysis_json_str = analysis_json_str.split("```json")[1].split("```")[0]
        
        analysis_data = json.loads(analysis_json_str.strip())

    except Exception as e:
        print(f"Agent 1 (Step 1) Error: {e}")
        analysis_data = {"mood_keywords": ["neutral"], "color_keywords": [], "content_keywords": []}


    # --- STEP 2: Text model generates the safe response ---
    try:
        # Create the prompt for the text model
        final_prompt = TEXT_PROMPT_TEMPLATE_ES.format(analysis=str(analysis_data))
        
        text_response = ollama_client.chat(
            model=AGENT_1_TEXT_MODEL,
            messages=[
                {
                    'role': 'user',
                    'content': final_prompt
                }
            ]
        )
        return text_response['message']['content']

    except Exception as e:
        print(f"Agent 1 (Step 2) Error: {e}")
        # Fallback in case of error
        return "Thank you for sharing your work. What was on your mind as you were creating this piece?"