from pydantic import BaseModel



class AccountForSignup(BaseModel):
    username: str
    password: str
# 测试账号：mystring，123456


class AccountForLogin(AccountForSignup):
    pass


# 限制登陆返回的格式（不限制的话会把整行返回）
class AccountPlublic(BaseModel):
    username: str
    id: int