# backend/core/config.py
# from core.config import settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DS API"
    api_key: str
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()

