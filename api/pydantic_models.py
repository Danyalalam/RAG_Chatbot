from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, Dict, List

class ModelName(str, Enum):
    LLAMA = "llama-3.1"  # Keeping the same value for API consistency

class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = None  # Optional with None default
    model: ModelName = ModelName.LLAMA  # Default to LLaMA
    

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName
    metrics: Optional[Dict[str, float]] = None  # Only current metrics

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int

class EvaluationRecord(BaseModel):
    id: int
    model: str
    question: str
    answer: str
    response_time: float
    tokens_used: int
    relevance_score: float
    citation_accuracy: float
    timestamp: datetime

# New model for evaluations with metrics dictionary
class EvaluationResponse(BaseModel):
    id: int
    model: str
    question: str
    answer: str
    metrics: Dict[str, float]
    timestamp: datetime