import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI Configuration (needed for embeddings)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = "https://langrag.openai.azure.com/"
AZURE_API_VERSION = "2024-02-15-preview"

# Embedding model info
EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
EMBEDDING_MODEL = "text-embedding-3-small"

# Groq API Key for LLaMA model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"