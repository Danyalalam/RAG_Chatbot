import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # Set model value directly without selection UI
    st.session_state.model = "llama-3.1"  # Keep consistent with ModelName enum
    
    # Display model info 
    st.sidebar.info("Using LLaMA 3.3 70B Versatile model")
    
    # Document Upload Section
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html", "txt"])
    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}.")
                    st.session_state.documents = list_documents()

    # Document List Section
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    # Display and Delete Documents
    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"📄 {doc['filename']}")
        
        # Delete Document
        selected_file_id = st.sidebar.selectbox(
            "Select a document to delete", 
            options=[doc['id'] for doc in documents],
            format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x)
        )
        
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                if delete_document(selected_file_id):
                    st.sidebar.success("Document deleted successfully!")
                    st.session_state.documents = list_documents()  # Refresh list
                else:
                    st.sidebar.error("Failed to delete document.")