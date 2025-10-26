# 🎨 Art Therapy Multi-Agent Chatbot

This is the backend and frontend prototype for a multi-agent AI system designed to assist with art therapy.

The goal is to provide a client with a simple chatbot to "journal" about a piece of art they've created as "homework." The AI guides the user through a brief reflection, and then summarizes the conversation. This allows both the client to do pre-session work and the therapist to get a concise summary, making the actual therapy session more focused and efficient.

## ⚙️ Technology Stack

- **Backend:** **FastAPI** (Python)
- **AI Model Serving:** **Ollama**
- **Frontend:** Plain **HTML, CSS, & JavaScript** (for this prototype)
- **AI Models:**
  - **Agent 1 (Vision):** `qwen2.5vl:3b` (The "eyes" that analyze the image)
  - **Agent 1 (Text):** `phi3:mini` (The "brain" that writes the safe first message)
  - **Agent 2 (Chat):** `phi3:mini` (The conversationalist)
  - **Agent 3 (Summary):** `phi3:mini` (The clinical summarizer)

## 🗂️ Project Structure

This project is a monorepo containing both the backend and frontend.

art_therapy_project/
├── backend/
│ ├── app/
│ │ ├── agents/
│ │ │ ├── **init**.py
│ │ │ ├── agent_1_vision.py  
│ │ │ ├── agent_2_chat.py  
│ │ │ ├── agent_3_summary.py  
│ │ ├── models/
│ │ │ ├── **init**.py
│ │ │ └── schemas.py  
│ │ ├── services/
│ │ │ ├── **init**.py
│ │ │ └── ollama_client.py  
│ │ └── **init**.py
│ ├── main.py  
│ └── requirements.txt  
│
├── frontend/
│ └── index.html  
│
└── README.md

---

## 🚀 Setup & Installation Guide

Follow these steps exactly to get the entire application running on your local machine.

### Step 1: Install Ollama (The AI Engine)

This is the most important prerequisite. Ollama runs the AI models locally.

1.  Go to [https://ollama.com/](https://ollama.com/) and download the app for your OS (Mac, Windows, or Linux).
2.  Install it. Once installed, **Ollama automatically runs in the background** and starts a server at `http://localhost:11434`. Our Python code is already configured to connect to this address.

### Step 2: Download the AI Models

Once Ollama is running, you must download the models we need. Open your terminal and run these commands one by one.

```bash
# This is the "eyes" for Agent 1 (approx 3.2 GB)
ollama pull qwen2.5vl:3b

# This is the "brain" for all agents (approx 2.3 GB)
ollama pull phi3:mini
```

You only need to do this once.

### Step 3: Set Up the Project & Git

1.  Open a terminal in the main `art_therapy_project/` folder.
2.  Initialize a new Git repository:
    ```bash
    git init
    ```
3.  Create a `.gitignore` file. This tells Git to ignore temporary files, secrets, and your virtual environment.
    ```bash
    touch .gitignore
    ```
4.  Copy and paste the following into your new `.gitignore` file:

    ```gitignore
    # Python
    __pycache__/
    *.pyc
    venv/
    *.env

    # Frontend (for later)
    frontend/node_modules/
    frontend/dist/

    # OS files
    .DS_Store
    ```

### Step 4: Set Up the Backend (Python)

1.  In your terminal, navigate **into** the `backend/` folder:
    ```bash
    cd backend
    ```
2.  Create a Python virtual environment. This keeps all your Python packages in a safe, isolated place.
    ```bash
    python3 -m venv venv
    ```
3.  Activate the virtual environment to "turn it on":

    - **On Mac/Linux:** `source venv/bin/activate`
    - **On Windows (Git Bash):** `source venv/Scripts/activate`
    - **On Windows (CMD):** `.\venv\Scripts\activate`

    (Your terminal prompt should now show `(venv)`.)

4.  Install all the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🏃 How to Run the Application

You'll need to run the backend and frontend separately.

### 1. Run the Backend Server

1.  Make sure you are in the `backend/` folder and your virtual environment is **active** (you see `(venv)` in your prompt).
2.  Run the FastAPI server using Uvicorn:

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    - `--reload`: Automatically restarts the server when you save code.
    - `--host 0.0.0.0`: Makes the server accessible from your frontend.

3.  Your backend is now running! You can see the auto-generated API docs at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

### 2. Run the Frontend App

1.  Navigate to the `frontend/` folder in your file explorer.
2.  **Just double-click the `index.html` file** to open it in your web browser (like Chrome or Firefox).

That's it! The chatbot in your browser will connect to your backend server, and you can start your first conversation by uploading an image.

---

## 🤖 How It Works: The Multi-Agent Flow

The entire application is a chain of 3 "agents" (specialized AI prompts) that hand off work to each other.

### Agent 1: The Vision & Starter

This agent's job is to start the conversation safely. We use a **2-step chain** for maximum control:

1.  **"Eyes" (`qwen2.5vl:3b`):** The frontend sends the image to the `/start_conversation` endpoint. This model analyzes the image with a strict prompt, forcing it to _only_ output a JSON object of keywords (e.g., `{"mood_keywords": ["dark", "chaotic"], ...}`).
2.  **"Brain" (`phi3:mini`):** The backend takes this JSON and feeds it to `phi3:mini` with a safe, rule-based system prompt. This prompt tells the AI, "If the mood is 'dark', start by gently asking 'How are you feeling today?'" This prevents the AI from making unsafe or wild guesses.

### Agent 2: The Chatbot

This agent handles the main conversation.

1.  Every time the user sends a message, the frontend sends the _entire_ chat history to the `/chat` endpoint.
2.  **`phi3:mini`** (acting as Agent 2) receives this history along with a system prompt that tells it to be "a supportive and curious art therapy assistant."
3.  For this prototype, we are **not** fine-tuning. We are using the powerful base `phi3:mini` model with a strong system prompt, which is more than enough to create a working prototype.

### Agent 3: The Summarizer

This agent's job is to create the clinical summary for the therapist.

1.  A separate (future) button in the app would send the _entire_ chat history to the `/summarize` endpoint.
2.  **`phi3:mini`** (acting as Agent 3) receives the history with a different system prompt, one that tells it to act as a "clinical assistant" and extract specific key points (Emotions, Insights, Topics for discussion) and format them as Markdown.

## ❓ What is an API Endpoint?

An **endpoint** is just a specific **URL** on your server that performs **one specific action**.

Think of your whole backend server (`http://localhost:8000`) as an **office building**. An endpoint is like a **specific door with a label** on it. Our `main.py` file defines these "doors":

- `GET /`: The "front door." Just says the API is running.
- `POST /start_conversation`: The "Art Upload" door. You send an image here, and it returns the first chat message.
- `POST /chat`: The "Chat" door. You send the conversation history here, and it returns the AI's next reply.
- `POST /summarize`: The "Therapist's" door. You send the conversation history here, and it returns the final clinical summary.
