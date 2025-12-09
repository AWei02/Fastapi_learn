from fastapi import APIRouter, Request, Cookie, Response, status, HTTPException, Depends

router = APIRouter()

@router.get("/")
async def root_api():
    return {"message": "依赖tab"}


# 验证cookie
def check_user(pan_token: str | None = Cookie(default=None)):
    print(pan_token)
    if pan_token != "FastAPI":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return pan_token


# 依赖项必然优先于加载函数
@router.get("/temp")
async def temp(*, token: str = Depends(check_user)):
    return {"message": "Hello World"}


# 设置cookie
@router.get("/set")
async def set_coo(resp: Response):
    resp.set_cookie(key="pan_token", value="FastAPI", expires=60,)
    return {"message": "set"}


# 依赖项层级判断
def level_1():
    print("level_1")  # level_1被执行了两次，但在缓存中，所以仅打印一次
    return 10


def level_2a(t2a: int = Depends(level_1)):
    print("level_2a")
    return 20 + t2a


def level_2b(t2b: int = Depends(level_1)):
    print("level_2b")
    return 40 + t2b


def level_3(l2b: int = Depends(level_2b), l2a: int = Depends(level_2a)):
    print("level_3")
    return l2a + l2b


# 用函数作为依赖项
def query_depends(user: str, token: str):
    data = {
        'user': user,
        'token': token,
    }
    return data


@router.get("/level")
async def level(total: int = Depends(level_3), common: str = Depends(query_depends)):
    print('total...')
    data = {
        'total': total,
        'common': common,
    }
    return data

# 将"类"作为依赖项，查询结果同上。说明依赖项的定义可用“类”，也可用“函数”
class User:
    def __init__(self, name: str, token: str):
        self.name = name
        self.token = token


@router.get("/depends_show")
async def depends_show(total: int = Depends(level_3), common: User = Depends(User)):
    print('total...')
    data = {
        'total': total,
        'name': common.name,
        'token': common.token,
    }
    return data


# 依赖项还可以放在路径装饰器里(list中展示)，但没有返回值
@router.get("/depends_show_1", dependencies=[Depends(level_3)])
async def depends_show_1(common: User = Depends(User)):
    print('total...')
    data = {
        'name': common.name,
        'token': common.token,
    }
    return data


# 简单应用