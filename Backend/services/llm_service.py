# backend/services/llm_service.py
from core.config import settings

def summarize_text(text: str) -> str:
    # placeholder for LLM provider
    return f"Summary of: {text[:50]}"