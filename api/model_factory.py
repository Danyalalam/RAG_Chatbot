from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Bedrock
from config import *
import logging

class ModelFactory:
    @staticmethod
    def get_model(model_name: str):
        try:
            if model_name == "gpt-4":
                return AzureChatOpenAI(
                    azure_deployment=GPT4_DEPLOYMENT,
                    api_version=AZURE_API_VERSION,
                    temperature=0.2,
                    max_tokens=50,  
                    azure_endpoint=AZURE_OPENAI_ENDPOINT,
                    api_key=AZURE_OPENAI_API_KEY
                )
            elif model_name == "llama-3.1":
                return ChatGroq(
                    api_key=GROQ_API_KEY,
                    model_name="llama-3.1-70b-versatile",
                    temperature=0.2,
                    max_tokens=500
                )
            elif model_name == "gemini-pro":
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                    google_api_key=GOOGLE_API_KEY
                )
            else:
                raise ValueError(f"Unknown model: {model_name}")
        except Exception as e:
            logging.error(f"Error initializing model {model_name}: {str(e)}")
            raise