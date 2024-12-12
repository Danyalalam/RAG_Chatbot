# test_azure_gpt4.py
from langchain_openai import AzureChatOpenAI
from config import *

def test_gpt4_response():
    try:
        # Initialize the model
        llm = AzureChatOpenAI(
            azure_deployment=GPT4_DEPLOYMENT,
            api_version=AZURE_API_VERSION,
            temperature=0.2,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY
        )

        # Test simple completion
        response = llm.invoke("Hi! Can you respond with a simple hello?")
        print("Response:", response)
        return True

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing GPT-4 connection...")
    success = test_gpt4_response()
    print(f"Test {'successful' if success else 'failed'}")