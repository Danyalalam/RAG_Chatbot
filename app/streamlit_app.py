import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface
from visualization import display_evaluation_charts

st.title("Multi-Model RAG Chatbot")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "model" not in st.session_state:
    st.session_state.model = "gpt-4"  # Default to GPT-4

# Display components
display_sidebar()


# Main Area Navigation
menu = ["Chat", "Evaluation"]
choice = st.sidebar.radio("Navigate", menu)

if choice == "Chat":
    display_chat_interface()
elif choice == "Evaluation":
    display_evaluation_charts()