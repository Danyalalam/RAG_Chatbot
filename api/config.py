import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = "https://langrag.openai.azure.com/"
AZURE_API_VERSION = "2024-02-15-preview"

# Model Deployments
GPT4_DEPLOYMENT = "gpt-4"
EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
EMBEDDING_MODEL = "text-embedding-3-small"

# Other Model Configs
LLAMA_MODEL_PATH = "path/to/llama/model"
AWS_PROFILE = "default"