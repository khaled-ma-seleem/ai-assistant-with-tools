import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Model configurations
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite-preview-06-17")
    LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3.2:3b")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Data paths
    VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "./data/vectorstore_index")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./data/uploaded_docs")
    CHECKPOINT_DB = os.getenv("CHECKPOINT_DB", "./data/checkpoints/checkpoint.db")
    
    # Create directories if they don't exist
    @classmethod
    def create_directories(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(cls.CHECKPOINT_DB), exist_ok=True)
        os.makedirs(os.path.dirname(cls.VECTORSTORE_PATH), exist_ok=True)