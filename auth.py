from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# pip install pyjwt
import jwt

SECRET_KEY = "c04db91a1b01a9ba0e847642c549d29eb37d8e6936eac621281353b8dfff738c"  # 32位随机密钥
# 命令行执行：openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 过期时间30分钟


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # 从请求头中获取Authorization的字段（以Bearer开头的）
# tokenUrl="/login"是为了方便在swaggerUI中右上角的Authorize按钮中测试，其实很麻烦，不推荐


# 创建token
def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    encode_jwt = jwt.encode(
        to_encode,  # 要通过token传输的内容
        SECRET_KEY,  # JWT签名的密钥
        algorithm = ALGORITHM,  # JWT签名的算法
    )
    return encode_jwt
# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImphY2siLCJleHAiOjE3NjUxOTQxNTB9.rLi0-LFDz8uy1SjrHTj8-jP05qi8ABGCn-fibjFk5A4"
# 由两个.区分开，可在https://www.jwt.io/中查看
# 第一部分：头部
# 第二部分：有效负荷
# 第三部分：加密签名（对前两部分验证，防止篡改）
# JWT工作本质：在请求头中的Authorization的字段（以Bearer开头的）读取解析，得到结果
# 仅负责：生成JWT、解码JWT、验证过期时间，无所谓签名怎么传递（请求头、url查询参数）
# 推荐用“请求头”传递的原因：跨域


## 验证token(verify_token)
# def get_user_token(token: str = Depends(oauth2_scheme)):
#     # print(token)  # 请求头中的Authorization的字段（以Bearer开头的）
#     payload = jwt.decode(
#         token,
#         SECRET_KEY,
#         algorithms=[ALGORITHM]
#     )
#     return payload


## 另外一种定义方式【验证token(verify_token)】
# 验证token(verify_token)
# def get_user_token(token: str):
#     payload = jwt.decode(
#         token,
#         SECRET_KEY,
#         algorithms=[ALGORITHM]
#     )
#     return payload


## 过期验证，记得修改过期时间
def get_user_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload