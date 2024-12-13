# test_groq_llama.py
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import time

def test_groq_llama():
    try:
        # Initialize Groq LLM
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )
        
        # Test query
        test_prompt = "What is machine learning?"
        print("Sending test query to LLaMA via Groq...")
        
        start_time = time.time()
        response = llm.invoke(test_prompt)
        end_time = time.time()
        
        print(f"\nResponse time: {end_time - start_time:.2f} seconds")
        print(f"\nResponse:\n{response}")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    load_dotenv()
    test_groq_llama()