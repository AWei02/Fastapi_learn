# 判断能否连接上
import redis

# 创建 Redis 连接并提供密码
r = redis.Redis(
    host='localhost',   # 或者你的 Redis 服务器的实际 IP 地址
    port=6379,          # 默认端口是 6379，请根据实际情况调整
    password='kfcv50',    # 这里填写你的 Redis 密码
    db=0                # 使用默认数据库，如有需要可更改
)

# 测试连接和认证是否成功
try:
    r.ping()  # 发送一个 PING 命令，检查能否成功连接到 Redis 服务器
    print("连接成功")
except redis.AuthenticationError:
    print("认证失败，请检查密码")
except redis.ConnectionError:
    print("无法连接到 Redis 服务器")