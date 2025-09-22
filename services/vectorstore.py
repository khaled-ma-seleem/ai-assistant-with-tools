import os
import shutil
import requests
import easyocr
import pandas as pd
from io import BytesIO
from PIL import Image
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from config import Config

class VectorStoreManager:
    """Manages vector store operations and document processing"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        self.vectorstore = None
        self.ocr_reader = None
    
    def create_or_load_vectorstore(self):
        """Loads an existing FAISS vectorstore from disk, or creates a new one if not found"""
        if os.path.exists(Config.VECTORSTORE_PATH):
            self.vectorstore = FAISS.load_local(
                Config.VECTORSTORE_PATH, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        else:
            self.vectorstore = None
        return self.vectorstore
    
    def save_vectorstore(self):
        """Saves the current FAISS vectorstore to disk"""
        if self.vectorstore:
            self.vectorstore.save_local(Config.VECTORSTORE_PATH)
    
    def reset_vectorstore(self):
        """Deletes the existing vectorstore directory from disk"""
        if os.path.exists(Config.VECTORSTORE_PATH):
            shutil.rmtree(Config.VECTORSTORE_PATH)
            self.vectorstore = None
            return "Vectorstore reset complete."
        else:
            return "No vectorstore to reset."
    
    def load_and_split_document(self, file_path: str):
        """Loads and splits a PDF or HTML file into smaller chunks for embedding"""
        if file_path.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.lower().endswith((".html", ".htm")):
            loader = UnstructuredHTMLLoader(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and HTML are supported.")
        
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
        return splitter.split_documents(documents)
    
    def add_document_to_vectorstore(self, file_path: str):
        """Adds a new PDF or HTML file's contents to the vector store and saves it"""
        docs = self.load_and_split_document(file_path)
        
        if not self.vectorstore:
            self.create_or_load_vectorstore()
        
        if self.vectorstore:
            self.vectorstore.add_documents(docs)
        else:
            self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        
        self.save_vectorstore()
        return f"Added {file_path} to vectorstore."
    
    def search_documents(self, query: str) -> str:
        """Search relevant information from the document store"""
        if not self.vectorstore:
            self.create_or_load_vectorstore()
        
        if not self.vectorstore:
            return "No documents in vectorstore. Please add some documents first."
        
        retriever = self.vectorstore.as_retriever(search_type="similarity", k=3)
        docs = retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in docs)
    
    @staticmethod
    def load_dataframe(filepath: str) -> pd.DataFrame:
        """Load a pandas DataFrame from a CSV file"""
        return pd.read_csv(filepath)