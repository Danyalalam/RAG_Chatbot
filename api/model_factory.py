from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
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
            elif model_name == "llama-3.1":  # Using LLaMA 3.1 via Groq
                return ChatGroq(
                    api_key=GROQ_API_KEY,
                    model_name="llama-3.1-70b-versatile",
                    temperature=0.2,
                    max_tokens=500
                )
            elif model_name == "anthropic.claude-v2":
                return Bedrock(
                    model_id="anthropic.claude-v2",
                    credentials_profile_name=AWS_PROFILE,
                    temperature=0.2,
                    max_tokens=500
                )
            else:
                raise ValueError(f"Unknown model: {model_name}")
        except Exception as e:
            logging.error(f"Error initializing model {model_name}: {str(e)}")
            raise