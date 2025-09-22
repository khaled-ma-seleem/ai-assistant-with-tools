from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama.chat_models import ChatOllama
from config import Config

class LLMFactory:
    """Factory class for creating LLM instances"""
    
    @staticmethod
    def create_llm(model_name: str, google_api_key: str = ""):
        """
        Creates and returns an LLM instance based on the specified model name.
        
        Args:
            model_name (str): Either 'llama' or 'gemini'
            google_api_key (str): API key for Gemini (optional for Llama)
            
        Returns:
            LLM instance
        """
        if model_name.lower() == "llama":
            return ChatOllama(model=Config.LLAMA_MODEL)
        
        elif model_name.lower() == "gemini":
            api_key = google_api_key or Config.GOOGLE_API_KEY
            if not api_key:
                raise ValueError("Google API key is required for Gemini model")
                
            return ChatGoogleGenerativeAI(
                model=Config.GEMINI_MODEL,
                google_api_key=api_key,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )
        
        else:
            raise ValueError("Unsupported model_name. Use 'llama' or 'gemini'.")
    
    @staticmethod
    def get_available_models():
        """Returns list of available model names"""
        return ["llama", "gemini"]