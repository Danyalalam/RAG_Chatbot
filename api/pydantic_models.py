from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# pydantic_models.py
class ModelName(str, Enum):
    GPT4 = "gpt-4"  
    LLAMA = "llama-3.1"
    BEDROCK = "gemini-pro"

class QueryInput(BaseModel):
    question: str
    session_id: str | None = None  # Make it optional with None default
    model: ModelName = ModelName.GPT4  # Set default

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int