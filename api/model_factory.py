from langchain_groq import ChatGroq
from config import *
import logging

class ModelFactory:
    @staticmethod
    def get_model(model_name: str):
        try:
            # Since we're using only LLaMA, we can simplify this logic
            return ChatGroq(
                api_key=GROQ_API_KEY,
                model_name="llama-3.3-70b-versatile",
                temperature=0.2,
                max_tokens=1024  # Set a specific value instead of None
            )
        except Exception as e:
            logging.error(f"Error initializing LLaMA model: {str(e)}")
            raise