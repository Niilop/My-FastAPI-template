# backend/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    # App Configuration
    app_name: str = "DS API"
    debug: bool = True
    
    # API Keys and Models
    api_key: SecretStr
    gemini_model: str
    
    # Database Configuration
    database_url: str
    
    # JWT Configuration
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS Origins
    cors_origins: list[str] = [
        "http://localhost:8501", 
        "http://127.0.0.1:8501",
        "http://localhost:3000"
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    return Settings()