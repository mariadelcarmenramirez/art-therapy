art_therapy_project/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── agent_1_vision.py   
│   │   │   ├── agent_2_chat.py     
│   │   │   ├── agent_3_summary.py  
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py          
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── ollama_client.py     
│   │   └── __init__.py
│   ├── main.py                      
│   └── requirements.txt            
│
├── frontend/
│   └── index.html                  
│
└── README.md   

*ACTIVATE VIRTUAL ENVIRONMENT*
cd backend
venv/Scripts/activate

----
*How to Make Your Backend Run*

1. Open your terminal.
2. Navigate to your backend folder: cd art_therapy_project/backend
3. Activate your virtual environment: venv/Scripts/activate
4. Run the Uvicorn server:
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
That's it. Your server is now running. You can open http://localhost:8000 in your browser to see the "API is running" message or http://localhost:8000/docs to see the API documentation.

*Download the LLM (I only need to do this once)* -> How to download them in the GPU? 
```
ollama pull qwen2.5vl:3b
ollama pull phi3:mini
```