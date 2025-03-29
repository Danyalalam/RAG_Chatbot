import requests
import streamlit as st
import time

# Define backend URL for local testing
# Use localhost:8000 which is the default FastAPI port
BACKEND_URL = "http://localhost:8000"
MAX_RETRIES = 2
RETRY_DELAY = 1  # seconds

def get_api_response(question, session_id, model):
    data = {
        "question": question,
        "session_id": session_id,
        "model": model  # Should match ModelName enum values exactly
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                headers={'Content-Type': 'application/json'},
                json=data,
                timeout=30  # Add timeout to prevent hanging requests
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Request payload: {data}")  # Debug print
            if attempt < MAX_RETRIES - 1:
                st.warning(f"Retrying in {RETRY_DELAY} seconds... (Attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
                continue
            st.error(f"API request failed: {str(e)}")
            return None
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to the backend at {BACKEND_URL}. Is your FastAPI server running?")
            if attempt < MAX_RETRIES - 1:
                st.warning(f"Retrying in {RETRY_DELAY} seconds... (Attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
                continue
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return None

def upload_document(file):
    print("Uploading file...")
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(
            f"{BACKEND_URL}/upload-doc",
            files=files,
            timeout=60  # Add timeout for file uploads
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the backend at {BACKEND_URL}. Is your FastAPI server running?")
        return None
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")
        return None

def list_documents():
    try:
        response = requests.get(f"{BACKEND_URL}/list-docs", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch document list. Error: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the backend at {BACKEND_URL}. Is your FastAPI server running?")
        return []
    except Exception as e:
        st.error(f"An error occurred while fetching the document list: {str(e)}")
        return []

def delete_document(file_id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {"file_id": file_id}

    try:
        response = requests.post(
            f"{BACKEND_URL}/delete-doc",
            headers=headers,
            json=data,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document. Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the backend at {BACKEND_URL}. Is your FastAPI server running?")
        return None
    except Exception as e:
        st.error(f"An error occurred while deleting the document: {str(e)}")
        return None