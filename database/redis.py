import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError


# 配置连接池
# 配置文件应放在.env中，小主机配置
# redis_pool = redis.ConnectionPool(
#     host='localhost',   # 或者你的 Redis 服务器的实际 IP 地址
#     port=6379,          # 默认端口是 6379，请根据实际情况调整
#     password='kfcv50',    # 这里填写你的 Redis 密码
#     decode_responses=True,  # redis转码字符串，默认返回值是字节码
#     encoding='utf-8'
# )

# 办公配置
redis_pool = redis.ConnectionPool(
    host='localhost',   # 或者你的 Redis 服务器的实际 IP 地址
    port=6379,          # 默认端口是 6379，请根据实际情况调整
    password='1234',    # 这里填写你的 Redis 密码
    decode_responses=True,  # redis转码字符串，默认返回值是字节码
    encoding='utf-8'
)

async def redis_connect():
    try:
        redis_client = redis.Redis(connection_pool=redis_pool)
        sig = await redis_client.ping()
        print(f"redis:{sig}")
        return redis_client
    except ConnectionError:
        print('redis连接失败')
    except TimeoutError:
        print('redis连接超时')   
    except Exception as e:
        print('redis连接异常')


# 缓存验证
from time import sleep
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/redis")
async def redis_set(request: Request):
    value = await request.app.state.redis.get("fastapi_redis")

    # 如果没用被redis缓存
    if value is None:
        sleep(5)
        hi = "hey,redis"
        await request.app.state.redis.set(
            "fastapi_redis",  # 键名
            hi,  # 键值
            ex=60,  # 过期时间（秒）
        )
    return value
