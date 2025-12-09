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


TORTOISE_MODELS = []

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
    'use_tz': False,
    'timezone': 'Asiz/Shanghai',
}


@asynccontextmanager
async def register_mysql(app: FastAPI):
    try:
        async with RegisterTortoise(
            app,
            config=TORTOISE_CONFIG,
            generate_schemas=True,  # 根据数据模型的类建立数据表，生产环境中应为false
        ):
            yield print("mysql连接成功")
            await connections.close_all()
            print("mysql已经关闭")
    except Exception as e:
        print(e)