from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ConversationHistory, ChatMessage, StartResponse
from app.agents import agent_1_vision, agent_2_chat, agent_3_summary
import uvicorn

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
    Agent 3: Receives the final, full conversation and returns
    a clinical summary for the therapist.
    """
    try:
        summary_message = await agent_3_summary.get_summary_response(history)
        return summary_message
    except Exception as e:
        print(f"Error in /summarize: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("--- Starting Art Therapy Backend Server ---")
    print("Access API docs at http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)