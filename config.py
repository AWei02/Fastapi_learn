from pydantic_settings import BaseSettings
from functools import lru_cache



class Settings(BaseSettings):
    # 各类声明
    DEBUG_MODE: bool = True
    STATIC_DIR: str = "static123"

    # 数据库
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # 邮件配置
    MAIL_USERNAME: str  # 用户名
    MAIL_PASSWORD: str  # 密码
    MAIL_FROM: str  # 从哪个地址发送（方便接收人回复）
    MAIL_SERVER: str  # smtp地址

    class Config:
        env_file=(".env", ".env.prod")


@lru_cache
def get_settings() -> Settings:
    return Settings()


config = get_settings()