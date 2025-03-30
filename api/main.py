from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import (
    QueryInput,
    QueryResponse,
    DocumentInfo,
    DeleteFileRequest,
)
from langchain_utils import get_rag_chain
import os
from db_utils import (
    insert_application_logs,
    get_chat_history,
    get_all_documents,
    insert_document_record,
    delete_document_record,
    fetch_all_evaluations
)
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma, vectorstore
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager  # Add this import
from keep_alive import KeepAliveService

import os
import uuid
import logging
import time
import shutil
from typing import List

logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize keep-alive service
keep_alive_service = KeepAliveService(interval_minutes=5)

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    keep_alive_service.start()
    logging.info("Application started, keep-alive service initialized")
    
    yield  # This is where the app runs
    
    # Shutdown code
    keep_alive_service.stop()
    logging.info("Application shutting down, keep-alive service stopped")

# Pass the lifespan to FastAPI
app = FastAPI(lifespan=lifespan)

# Define allowed origins
origins = [
    "http://localhost",            # For local testing
    "http://localhost:8501",       # Streamlit default port
    "https://*.streamlit.app"      # For Streamlit Cloud deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a health endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint that the keep-alive service will ping"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    start_time = time.time()  # Start timer for response time
    
    # Generate session_id if None
    session_id = query_input.session_id or str(uuid.uuid4())
    
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")
    
    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(query_input.model.value)
    
    # Retrieve relevant documents (Assuming get_rag_chain handles context retrieval)
    answer = rag_chain.invoke({
        "input": query_input.question,
        "chat_history": chat_history
    })['answer']
    
    # Insert logs with evaluation metrics
    insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
    
    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    
    return QueryResponse(
        answer=answer, 
        session_id=session_id, 
        model=query_input.model,
    )

@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf', '.docx', '.html']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}")
    
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_id = insert_document_record(file.filename)
        success = index_document_to_chroma(temp_file_path, file_id)
        
        if success:
            return {"message": f"File {file.filename} has been successfully uploaded and indexed.", "file_id": file_id}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/list-docs", response_model=List[DocumentInfo])
def list_documents():
    return get_all_documents()

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    # Delete from Chroma
    chroma_delete_success = delete_doc_from_chroma(request.file_id)

    if chroma_delete_success:
        # If successfully deleted from Chroma, delete from our database
        db_delete_success = delete_document_record(request.file_id)
        if db_delete_success:
            return {"message": f"Successfully deleted document with file_id {request.file_id} from the system."}
        else:
            return {"error": f"Deleted from Chroma but failed to delete document with file_id {request.file_id} from the database."}
    else:
        return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma."}

