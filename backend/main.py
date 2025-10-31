from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ConversationHistory, ChatMessage, StartResponse
from app.agents import agent_1_vision, agent_2_chat, agent_3_summary
import uvicorn
import os  # <-- ADDED for directory/file operations
from datetime import datetime  # <-- ADDED for timestamping

# Initialize the FastAPI app
app = FastAPI(
    title="Art Therapy Chatbot API",
    description="Backend for the multi-agent art therapy assistant.",
)

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Directory for saving summaries ---
SUMMARY_DIR = "summaries"
# ---

@app.get("/")
async def root():
    return {"message": "Art Therapy API is running. Go to /docs for API documentation."}


@app.post("/start_conversation", response_model=StartResponse)
async def start_conversation(file: UploadFile = File(...)):
    """
    Agent 1: Receives an image, analyzes it, and returns the
    first message of the conversation.
    """
    try:
        image_bytes = await file.read()
        first_message = await agent_1_vision.get_conversation_starter(image_bytes)
        return StartResponse(first_message=first_message)
    except Exception as e:
        print(f"Error in /start_conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatMessage)
async def chat(history: ConversationHistory):
    """
    Agent 2: Receives the full conversation history and returns
    the next assistant message.
    """
    try:
        response_message = await agent_2_chat.get_chat_response(history)
        return response_message
    except Exception as e:
        print(f"Error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize", response_model=ChatMessage)
async def summarize(history: ConversationHistory):
    """
    Agent 3: Receives the final, full conversation, returns
    a clinical summary, and saves it to a file.
    """
    try:
        # 1. Get the summary from Agent 3
        summary_message = await agent_3_summary.get_summary_response(history)
        summary_text = summary_message.content
        
        # 2. Create the summaries directory if it doesn't exist
        os.makedirs(SUMMARY_DIR, exist_ok=True)
        
        # 3. Create a timestamped filename (e.g., "2025-10-31_08-30-01.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}.txt"
        filepath = os.path.join(SUMMARY_DIR, filename)
        
        # 4. Save the summary content to the file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(summary_text)
            
        print(f"--- Summary saved to {filepath} ---") # Log for the server
        
        # 5. Return the summary to the frontend (as before)
        return summary_message
        
    except Exception as e:
        print(f"Error in /summarize: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("--- Starting Art Therapy Backend Server ---")
    print(f"--- Summaries will be saved to '{SUMMARY_DIR}' directory ---")
    print("Access API docs at http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)