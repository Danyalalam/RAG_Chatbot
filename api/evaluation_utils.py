import time
from typing import Dict, List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from db_utils import insert_evaluation_record
import nltk
from nltk.tokenize import word_tokenize

# Ensure NLTK resources are downloaded
nltk.download('punkt')

class ModelEvaluator:
    def __init__(self):
        # Initialize TfidfVectorizer without fitting on an empty string
        self.vectorizer = TfidfVectorizer()
    
    def evaluate_response(self, model: str, question: str, answer: str, 
                         start_time: float, tokens: int, context: List[str]):
        response_time = time.time() - start_time
        relevance = self._calculate_relevance(answer, context)
        citation_accuracy = self._verify_citations(answer, context)
        
        # Save evaluation metrics to the database
        insert_evaluation_record(
            model=model,
            question=question,
            answer=answer,
            response_time=response_time,
            tokens_used=tokens,
            relevance_score=relevance,
            citation_accuracy=citation_accuracy
        )
        
        return {
            "response_time": response_time,
            "tokens_used": tokens,
            "relevance_score": relevance,
            "citation_accuracy": citation_accuracy
        }
    
    def _calculate_relevance(self, answer: str, context: List[str]) -> float:
        """
        Calculate the relevance of the answer based on cosine similarity with context.
        Enhanced by using the average similarity instead of the maximum.
        """
        if context and any(doc.strip() for doc in context):
            try:
                # Fit the vectorizer on context documents
                self.vectorizer.fit(context)
                
                # Transform the answer and context documents into TF-IDF vectors
                answer_vec = self.vectorizer.transform([answer])
                context_vec = self.vectorizer.transform(context)
                
                # Compute cosine similarity between the answer and each context document
                similarities = cosine_similarity(answer_vec, context_vec)[0]
                
                # Use average similarity as the relevance score
                relevance_score = np.mean(similarities)
                
                return relevance_score
            except ValueError:
                # In case of any issues during vectorization
                return 0.0
        else:
            # If context is empty or only contains whitespace
            return 0.0
    
    def _verify_citations(self, answer: str, context: List[str]) -> float:
        """
        Calculate citation accuracy by checking the presence of context keywords in the answer.
        Enhanced by ensuring robust keyword extraction.
        """
        if not context:
            return 0.0
        
        # Combine all context documents into a single string and extract keywords
        context_text = ' '.join(context).lower()
        context_keywords = set(word_tokenize(context_text))
        
        # Extract keywords from the answer
        answer_text = answer.lower()
        answer_keywords = set(word_tokenize(answer_text))
        
        # Find common keywords between context and answer
        common_keywords = context_keywords.intersection(answer_keywords)
        
        if not context_keywords:
            return 0.0
        
        # Calculate the proportion of context keywords found in the answer
        citation_accuracy = len(common_keywords) / len(context_keywords)
        
        return citation_accuracy