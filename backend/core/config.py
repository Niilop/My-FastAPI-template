# backend/core/config.py
# from core.config import settings
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    app_name: str = "DS API"
    api_key: SecretStr
    debug: bool = True
    gemini_model: str
    
    cors_origins: list[str] = [
        "http://localhost:8501", 
        "http://127.0.0.1:8501"
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    return Settings()