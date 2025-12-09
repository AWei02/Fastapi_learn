from pydantic_settings import BaseSettings
from functools import lru_cache



class Settings(BaseSettings):
    # 各类声明
    DEBUG_MODE: bool = True
    STATIC_DIR: str = "static123"

    class Config:
        env_file=(".env", ".env.prod")


@lru_cache
def get_settings() -> Settings:
    return Settings()


config = get_settings()