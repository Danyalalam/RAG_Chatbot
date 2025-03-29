import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface

st.title("Congressional Data Analysis with LLaMA 3.3")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "model" not in st.session_state:
    st.session_state.model = "llama-3.1"  # Default to LLaMA

# Add a brief description about the specialized purpose
st.markdown("""
This RAG chatbot uses LLaMA 3.3 to analyze congressional voting records and legislative behavior.
Upload congressional data files to analyze voting patterns, party alignment, and legislative priorities.
""")

# Display components
display_sidebar()
display_chat_interface()