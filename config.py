"""
Configuration module for BEP Agent.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for BEP Agent application."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Embedding Configuration
    USE_LOCAL_EMBEDDINGS = os.getenv("USE_LOCAL_EMBEDDINGS", "false").lower() == "true"
    EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI embedding model
    LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence transformer model
    
    # Text Processing Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval Configuration
    TOP_K_CHUNKS = int(os.getenv("TOP_K_CHUNKS", "5"))
    TOP_K_PLANS = int(os.getenv("TOP_K_PLANS", "3"))
    
    # File Paths
    BEP_SAMPLES_DIR = "data/bep_samples"
    NEW_PROJECT_DIR = "data/new_project"
    VECTOR_STORE_PATH = "data/vector_store"
    
    # GPT Configuration
    GPT_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        if not cls.USE_LOCAL_EMBEDDINGS and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when not using local embeddings")
        
        # Create necessary directories
        os.makedirs(cls.BEP_SAMPLES_DIR, exist_ok=True)
        os.makedirs(cls.NEW_PROJECT_DIR, exist_ok=True)
        os.makedirs(cls.VECTOR_STORE_PATH, exist_ok=True)
        
        return True
