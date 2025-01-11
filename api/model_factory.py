from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from config import *
import logging

class ModelFactory:
    @staticmethod
    def get_model(model_name: str):
        try:
            if model_name == "gpt-4":
                return ChatOpenAI(
                    model_name="gpt-4",
                    openai_api_key=OPENAI_API_KEY,
                    temperature=0.2,
                    max_tokens=None
                )
            elif model_name == "llama-3.1":
                return ChatGroq(
                    api_key=GROQ_API_KEY,
                    model_name="llama-3.1-70b-versatile",
                    temperature=0.2,
                    max_tokens=None
                )
            elif model_name == "gemini-pro":
                return ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    temperature=0.2,
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