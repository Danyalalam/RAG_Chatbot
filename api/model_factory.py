# model_factory.py
from langchain_openai import AzureChatOpenAI
from langchain_community.llms import LlamaCpp
from langchain_community.llms import Bedrock
from config import *

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
            elif model_name == "llama-2":
                return LlamaCpp(
                    model_path=LLAMA_MODEL_PATH,
                    temperature=0.2,
                    n_ctx=2048,
                    verbose=True
                )
            elif model_name == "anthropic.claude-v2":
                return Bedrock(
                    model_id="anthropic.claude-v2",
                    credentials_profile_name=AWS_PROFILE,
                    temperature=0.2
                )
            else:
                raise ValueError(f"Unknown model: {model_name}")
        except Exception as e:
            print(f"Error initializing model {model_name}: {str(e)}")
            raise