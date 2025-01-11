import os
import logging
from chroma_utils import index_document_to_chroma, load_and_split_document
from db_utils import insert_document_record
from langchain_core.documents import Document

# Configure logging
logging.basicConfig(filename='load_existing_docs.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Directory containing the existing documents
DOCUMENTS_DIR = os.path.join(os.getcwd(), 'existing_docs')

def load_documents(directory: str):
    """
    Loads and indexes all supported documents in the specified directory.
    """
    supported_extensions = ['.pdf', '.docx', '.html']
    documents = [file for file in os.listdir(directory) if os.path.splitext(file)[1].lower() in supported_extensions]
    
    if not documents:
        logging.warning(f"No supported documents found in {directory}.")
        return
    
    for doc_file in documents:
        file_path = os.path.join(directory, doc_file)
        logging.info(f"Processing file: {doc_file}")
        
        try:
            # Insert document record into the database
            file_id = insert_document_record(doc_file)
            logging.info(f"Inserted document record for {doc_file} with file_id {file_id}.")
            
            # Index the document into ChromaDB
            success = index_document_to_chroma(file_path, file_id)
            if success:
                logging.info(f"Successfully indexed {doc_file} into ChromaDB.")
            else:
                logging.error(f"Failed to index {doc_file} into ChromaDB.")
        except Exception as e:
            logging.error(f"Error processing {doc_file}: {e}")

if __name__ == "__main__":
    load_documents(DOCUMENTS_DIR)
    logging.info("Completed loading existing documents into ChromaDB.")