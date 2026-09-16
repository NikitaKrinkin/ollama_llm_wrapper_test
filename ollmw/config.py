import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:1b")
    SYSTEM_PROMPT = os.getenv(
        "SYSTEM_PROMPT", 
        "Ты полезный технический ассистент. Отвечай кратко и понятно."
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key")
