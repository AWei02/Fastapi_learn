from passlib.context import CryptContext
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException, Response
from account.models import Account
from account.schemas import AccountForLogin, AccountForSignup, AccountPlublic


router = APIRouter()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")  # 定义加密方法，不使用废弃的方法


def get_password_hash(password: str):
    return pwd_context.hash(password)

# 用户名是否存在，存在返回用户数据，不存在返回none
async def is_username_existed(username: str):
    return await Account.get_or_none(username=username)




@router.post('/signup')
async def signup(account: AccountForSignup):
    user = await is_username_existed(account.username)
    if user:
        raise HTTPException(status_code=409, detail="用户名已存在")
    
    # 加密密码
    hashed_password = get_password_hash(account.password)

    # 保存用户名与加密以后的密码
    try:
        result = await Account.create(username=account.username, hashed_password=hashed_password)
        print(result.username)
        return Response(status_code=201, content="用户创建成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# 登陆
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

@router.post('/login', response_model=AccountPlublic)
async def login(account: AccountForLogin):
    # 检测用户是否存在
    user = await is_username_existed(account.username)
    if not user:
        raise HTTPException(status_code=404, detail="用户名不存在")
    
    if not verify_password(account.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名or密码错误")
    
    return user