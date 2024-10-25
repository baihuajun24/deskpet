import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AI Service Configuration
AI_SERVICE_CONFIG = {
    "type": os.getenv("AI_SERVICE_TYPE", "ollama"),  # "openai" or "ollama"
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "ollama_url": os.getenv("OLLAMA_URL", "http://localhost:11434")
}