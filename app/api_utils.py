import requests
import streamlit as st

def get_api_response(question, session_id, model):
    data = {
        "question": question,
        "session_id": session_id,
        "model": model  # Should match ModelName enum values exactly
    }
    
    try:
        response = requests.post(
            "https://rag-chatbot-leez.onrender.com/chat",  # Updated URL
            headers={'Content-Type': 'application/json'},
            json=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Request payload: {data}")  # Debug print
        st.error(f"API request failed: {str(e)}")
        return None

def upload_document(file):
    print("Uploading file...")
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(
            "https://rag-chatbot-leez.onrender.com/upload-doc",  # Updated URL
            files=files
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")
        return None

def list_documents():
    try:
        response = requests.get("https://rag-chatbot-leez.onrender.com/list-docs")  # Updated URL
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch document list. Error: {response.status_code} - {response.text}")
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
            "https://rag-chatbot-leez.onrender.com/delete-doc",  # Updated URL
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while deleting the document: {str(e)}")
        return None