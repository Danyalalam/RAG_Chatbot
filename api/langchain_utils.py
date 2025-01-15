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



# System prompt for contextualizing questions
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question, formulate a standalone question that will help retrieve relevant patterns, "
    "recurring themes, and personal insights across multiple journal entries. The reformulated question should emphasize: "
    "1. Long-term patterns and behavioral trends "
    "2. Emotional and psychological themes "
    "3. Decision-making patterns and their outcomes "
    "4. Personal growth and development insights "
    "Do NOT answer the question, only reformulate it if needed to maximize relevant context retrieval."
)

# Main QA prompt
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are analyzing personal journal entries to extract meaningful insights and patterns. 
    When analyzing the provided context:
    1. Focus on patterns and themes that are explicitly evidenced in the entries
    2. Connect related insights across different time periods
    3. Identify recurring behaviors, thoughts, and emotional patterns
    4. Note significant changes or transformations over time
    
    If certain aspects aren't directly supported by the context, focus on what is available in the provided entries."""),
    HumanMessagePromptTemplate.from_template(
        """Based on these journal entries and their context:
        {context}
        
        Provide an analysis addressing: {input}
        
        Focus on insights and patterns that are specifically supported by the provided entries."""
    ),
    MessagesPlaceholder(variable_name="chat_history")
])

# Question contextualization prompt
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    HumanMessagePromptTemplate.from_template(
        "Previous chat context: {chat_history}\n"
        "Current analysis request: {input}\n"
        "Reformulated question for context retrieval:"
    )
])


from model_factory import ModelFactory

def get_rag_chain(model_name: str):
    llm = ModelFactory.get_model(model_name)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain