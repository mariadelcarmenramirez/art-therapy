import ollama

# --- Centralized Model Configuration ---
# Qwen2.5-VL:3B for "eyes", Phi-3 Mini for all "brains
AGENT_1_VISION_MODEL = "qwen2.5vl:3b"
AGENT_1_TEXT_MODEL = "phi3:mini"
AGENT_2_CHAT_MODEL = "phi3:mini"
AGENT_3_SUMMARY_MODEL = "phi3:mini"
# ---

try:
    ollama_client = ollama.Client()
    ollama_client.list() 
    print("Ollama connection successful.")
except Exception as e:
    print(f"FATAL: Could not connect to Ollama.")
    print("Please make sure Ollama is running.")
    print(f"Error: {e}")
    ollama_client = None