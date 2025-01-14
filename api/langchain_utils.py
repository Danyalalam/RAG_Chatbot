from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,HumanMessagePromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vectorstore
retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

output_parser = StrOutputParser()




# Set up prompts and chains
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

qa_prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(
        "Use the following context to answer the user's question.\nContext: {context}\n\nQuestion: {input}"
    ),
    MessagesPlaceholder(variable_name="chat_history")
])

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(
        "Given a chat history and the latest user question, formulate a standalone question.\n"
        "Chat history: {chat_history}\n"
        "User question: {input}\n"
        "Standalone question:"
    )
])


from model_factory import ModelFactory

def get_rag_chain(model_name: str):
    llm = ModelFactory.get_model(model_name)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain