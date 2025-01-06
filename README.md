# 🤖 Multi-Model RAG Chatbot

A powerful Retrieval-Augmented Generation (RAG) chatbot that leverages multiple language models (GPT-4, LLaMA, Gemini) to provide context-aware responses based on uploaded documents.

## ✨ Features

- **Multi-Model Support**: Switch between GPT-4, LLaMA 3.1, and Gemini Pro
- **Document Management**: Upload, list, and delete PDF, DOCX, and HTML documents
- **RAG Implementation**: Uses ChromaDB for efficient document retrieval
- **Performance Analytics**: Visualize and compare model metrics
- **Interactive UI**: Built with Streamlit for a seamless user experience

## 🏗️ Architecture

RAG_Chatbot/ ├── api/ │ ├── main.py # FastAPI backend │ ├── chroma_utils.py # ChromaDB integration │ ├── models.py # Pydantic models │ └── database.py # SQLite database handling │ ├── app/ │ ├── streamlit_app.py # Main Streamlit application │ ├── api_utils.py # API interaction utilities │ ├── chat_interface.py # Chat UI component │ ├── sidebar.py # Sidebar component │ └── visualization.py # Analytics visualization │ └── requirements.txt # Project dependencies


## 🛠️ Tech Stack

- **Backend**: FastAPI, ChromaDB, SQLite
- **Frontend**: Streamlit
- **Models**: GPT-4, LLaMA 3.1, Gemini Pro
- **Data Processing**: LangChain, Pandas
- **Visualization**: Matplotlib, Seaborn

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RAG_Chatbot.git
cd RAG_Chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
copy .env.example .env
# Edit .env with your API keys
```