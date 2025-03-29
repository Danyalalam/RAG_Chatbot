from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vectorstore
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

output_parser = StrOutputParser()

# System prompt for contextualizing questions about congressional data
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question about congressional data, formulate a standalone question "
    "that will help retrieve relevant information about voting records, legislative patterns, and congressional behavior. "
    "The reformulated question should emphasize: "
    "1. Voting patterns and legislative priorities "
    "2. Party alignment and instances of cross-party voting "
    "3. Focus areas in policy-making and bill sponsorship "
    "4. Consistency or evolution of positions on key issues "
    "Do NOT answer the question, only reformulate it if needed to maximize relevant information retrieval from congressional records."
)

# Main QA prompt optimized for congressional data analysis
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are analyzing congressional data including voting records, bill information, and representative profiles. 
    When analyzing the provided context:
    1. Focus on factual voting patterns and legislative behavior that is evident in the records
    2. Identify consistent policy positions and any notable deviations
    3. Note relationships between party affiliation and voting behavior
    4. Provide insights on legislative priorities based on voting history and bill engagement
    5. Avoid speculation beyond what the data supports
    
    When discussing representatives' positions, remain politically neutral and focus only on the data presented."""),
    HumanMessagePromptTemplate.from_template(
        """Based on these congressional records:
        {context}
        
        Provide an analysis addressing: {input}
        
        Focus on insights and patterns that are specifically supported by the provided voting records and biographical information."""
    ),
    MessagesPlaceholder(variable_name="chat_history")
])

# Question contextualization prompt
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    HumanMessagePromptTemplate.from_template(
        "Previous chat context: {chat_history}\n"
        "Current analysis request: {input}\n"
        "Reformulated question for congressional data retrieval:"
    )
])

from model_factory import ModelFactory

def get_rag_chain(model_name: str):
    llm = ModelFactory.get_model(model_name)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain