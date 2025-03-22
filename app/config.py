from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./shortener.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SHORT_CODE_LENGTH: int = 6
    MAX_CUSTOM_ALIAS_LENGTH: int = 50
    ALLOWED_CUSTOM_ALIAS_PATTERN: str = r"^[a-zA-Z0-9_-]+$"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings() 