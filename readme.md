# 🎨 Art Therapy Multi-Agent Chatbot

This repository contains the **backend and frontend prototype** of a multi-agent AI system designed to support **art therapy sessions**.

The goal is to provide clients with a safe, reflective chatbot experience to “journal” about their artwork before therapy sessions. The AI guides users through a gentle reflection and then generates a **concise summary** for therapists, making the actual session more focused and efficient.

---

## ⚙️ Technology Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **AI Model Serving:** [Ollama](https://ollama.com/)
- **Frontend:** HTML, CSS, JavaScript (prototype only)
- **AI Models:**
  - **Agent 1 (Vision):** `qwen2.5vl:3b`
  - **Agent 1 (Text):** `phi3:mini`
  - **Agent 2 (Chat):** `phi3:mini`
  - **Agent 3 (Summary):** `phi3:mini`

---

## 🚀 Setup & Installation

Follow these steps to set up and run the entire application locally.

### 1. Install Ollama

1. Download and install **Ollama** for your OS from [https://ollama.com/](https://ollama.com/).  
2. Once installed, Ollama runs automatically in the background at  
   `http://localhost:11434`.

### 2. Download Required AI Models

Run the following commands in your terminal (after installing Ollama):

```bash
# Vision model (for image analysis)
ollama pull qwen2.5vl:3b

# Text model (used by all agents)
ollama pull phi3:mini
````

You only need to do this once.

### 3. Set Up the Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   ```

   * **Mac/Linux:** `source venv/bin/activate`
   * **Windows (CMD):** `.\venv\Scripts\activate`
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### 4. Run the Backend Server

With the virtual environment activated, start the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Once running, the API documentation will be available at:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Run the Frontend

1. Open the `frontend/` folder.
2. Double-click the `index.html` file to open it in your web browser.

The frontend will automatically connect to your local backend server.

---

## ✅ You’re Ready to Go!

You can now upload an artwork image, begin journaling with the AI chatbot, and receive an auto-generated reflection summary — all locally powered by Ollama.

---

> 💡 **Note:** This is a prototype for research and testing purposes. It is not intended for real therapeutic use without professional supervision.

