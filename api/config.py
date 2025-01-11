import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Azure OpenAI Configuration (if still needed for other models)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = "https://langrag.openai.azure.com/"
AZURE_API_VERSION = "2024-02-15-preview"

# Model Deployments
GPT4_DEPLOYMENT = "gpt-4"
EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
EMBEDDING_MODEL = "text-embedding-3-small"

# Other Model Configs
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = "llama-3.1-70b-versatile"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-1.5-pro"