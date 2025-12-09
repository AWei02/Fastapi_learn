from pydantic_settings import BaseSettings
from functools import lru_cache



class Settings(BaseSettings):
    # 各类声明
    DEBUG_MODE: bool = True
    STATIC_DIR: str = "static123"
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    class Config:
        env_file=(".env", ".env.prod")


@lru_cache
def get_settings() -> Settings:
    return Settings()


config = get_settings()