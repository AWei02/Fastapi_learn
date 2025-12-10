from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from tortoise import connections

from config import config


MYSQL_HOST = config.MYSQL_HOST
MYSQL_PORT = config.MYSQL_PORT
MYSQL_USER = config.MYSQL_USER
MYSQL_PASSWORD = config.MYSQL_PASSWORD
MYSQL_DATABASE = config.MYSQL_DATABASE


# 通过加载文件的方式引入models
# TORTOISE_MODELS = []
TORTOISE_MODELS = ["account.models"]

TORTOISE_CONFIG = {
    'connections': {
        'default': {
            "engine": 'tortoise.backends.mysql',
            'credentials': {
                'host': MYSQL_HOST,
                'port': MYSQL_PORT,
                'user': MYSQL_USER,
                'password': MYSQL_PASSWORD,
                'database': MYSQL_DATABASE,
            }
        },
    },

    'apps': {
        "tai_models": {
            'models': TORTOISE_MODELS,
            'default_connection': 'default',
        },
        # "db2": {
        #     'models': TORTOISE_MODELS,
        #     'default_connection': 'default',
        # }
    },
    'use_tz': False,  # 不使用默认时区
    'timezone': 'Asia/Shanghai',
}


@asynccontextmanager
async def register_mysql(app: FastAPI):
    try:
        print("开始初始化 MySQL 连接...")
        async with RegisterTortoise(
            app,
            config=TORTOISE_CONFIG,
            generate_schemas=True,  # 根据数据模型的类建立数据表，生产环境中应为false
        ):
            print("mysql连接成功")
            yield
            # await connections.close_all()
        print("mysql连接已由 RegisterTortoise 自动关闭")
    except Exception as e:
        print(f"MySQL 初始化失败: {e}")
        raise