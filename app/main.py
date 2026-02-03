from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil
import os
import uuid
from app.graph.workflow_graph import build_workflow_graph

app = FastAPI(title="Agentic Healthcare")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize graph once
graph = build_workflow_graph()

# Directory to store uploaded files temporarily
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/invoke")
async def invoke_workflow(
    raw_input: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    Trigger the healthcare agentic workflow with raw text input and optional file.
    """
    file_path = None
    if file:
        # Generate unique filename to avoid collisions
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
    try:
        initial_state = {
            "raw_input": raw_input,
            "file_input": os.path.abspath(file_path) if file_path else None
        }
        result = graph.invoke(initial_state)
        return result
    finally:
        # Optional: Cleanup file after processing if you want to save space
        # if file_path and os.path.exists(file_path):
        #     os.remove(file_path)
        pass
