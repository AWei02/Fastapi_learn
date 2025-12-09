from fastapi import APIRouter, Security, Depends, HTTPException, status, Cookie, Response, Request
from fastapi.security import SecurityScopes
from auth import create_token, get_user_token


router = APIRouter()

@router.get("/")
async def root_api():
    return {"message": "权限tab"}


## 无用的演示
# def security_test():
#     pass


# @router.get("/security", dependencies=[Security(security_test)])
# async def security(test=Security(security_test)):
#     return {"message": "权限tab"}
## ======================


## 通过scopes获取角色
# def print_scopes(security_scopes: SecurityScopes):
#     print(security_scopes.scopes)

# # scopes输入是list，可以为同一个路径，添加多个权限标识
# @router.get("/group/admin", dependencies=[Security(print_scopes, scopes=["admin", "bbb", "ccc"])])
# async def group_admin():
#     pass


# @router.get("/group/user", dependencies=[Security(print_scopes, scopes=["user"])])
# async def group_user():
#     pass


# @router.get("/group/guest", dependencies=[Security(print_scopes, scopes=["guest"])])
# async def group_guest():
#     pass
## ======================


## 角色的应用
# 验证是否含cookie
# def get_user_token(pan_token: str | None = Cookie(default=None)):
#     print(pan_token)
#     if pan_token is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无权限")
#     return pan_token


# # 验证cookie是否符合角色(在这里查询数据库)
# def get_user_permission(token: str = Depends(get_user_token)):
#     if token == "123":
#         return "admin"
#     if token == "456":
#         return "user"


# def check_user(security_scopes: SecurityScopes, user_permission: str = Depends(get_user_permission)):
#     if user_permission not in security_scopes.scopes:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无权限")


# @router.get("/test", dependencies=[Security(check_user, scopes=["admin", "bbb", "ccc"])])
# async def root_api():
#     return {"message": "admin权限"}

## ======================

## RBAC
# 一个用户可有多个角色
# ALL_USERS = {
#     "jack": ['admin', 'users'],
#     "rose": ['admin'],
#     "tom": ['users'],
#     "jerry": [],
# }

# # 一个角色可有多个权限（把权限放在路径接口上，让接口更独立，就可以通过角色分配权限）
# ROLE_PERMISSIONS = {
#     'admin': ['upload'],
#     "users": ['visit', 'download'],
# }

# # 设置cookie
# @router.get("/login", summary="模拟登陆")
# async def set_cookie(resp: Response, token: str):
#     resp.set_cookie(key="user_name", value=token, expires=600,)
#     return {"message": "set_cookie"}


# def get_user_token(user_name: str | None = Cookie(default=None)):
#     # print(user_name)
#     if user_name is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无权限")
#     return user_name


# # 查询角色的权限
# def get_role_permissions(role_name: list[str]):
#     print(role_name)
#     permissions = []
#     for role in role_name:
#         for perm in ROLE_PERMISSIONS[role]:
#             permissions.append(perm)
#             print(permissions)
#     return permissions


# # 查询用户的角色
# def get_user_permissions(token: str = Depends(get_user_token)):
#     if token in ALL_USERS:
#         return get_role_permissions(ALL_USERS[token])
#     return None


# def check_user(security_scopes: SecurityScopes, user_permission: str = Depends(get_user_permissions)):
#     # 先获取用户权限（前提通过Cookie获取用户名），有用户名就知道角色，知道角色就为他添加权限
#     for scope in security_scopes.scopes:
#         if scope not in user_permission:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无权限")


# @router.get("/upload", dependencies=[Security(check_user, scopes=['upload'])])
# async def upload():
#     return {"message": "upload权限"}


# @router.get("/visit", dependencies=[Security(check_user, scopes=['visit'])])
# async def visit():
#     return {"visit": "visit权限"}


# @router.get("/download", dependencies=[Security(check_user, scopes=['download'])])
# async def download():
#     return {"message": "download权限"}


## ======================

## JWT
ALL_USERS = {
    "jack": ['admin', 'users'],
    "rose": ['admin'],
    "tom": ['users'],
    "jerry": [],
}

# 一个角色可有多个权限（把权限放在路径接口上，让接口更独立，就可以通过角色分配权限）
ROLE_PERMISSIONS = {
    'admin': ['upload'],
    "users": ['visit', 'download'],
}

# 设置cookie
@router.get("/login", summary="模拟登陆")
async def set_cookie(resp: Response, token: str):
    resp.set_cookie(key="user_name", value=token, expires=600,)
    return {"message": "set_cookie"}


# def get_user_token(user_name: str | None = Cookie(default=None)):
#     # print(user_name)
#     if user_name is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无权限")
#     return user_name

# 最终版
def get_username(token: str = Depends(get_user_token)):
    user_name = token["username"]
    if user_name is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无权限")
    return user_name


# 用auth来控制权限（JWT）
@router.get("/send_token")
async def send_token(request: Request):
    
    data = {"username": "jack"}
    token = create_token(data)
    return token


## 用postman发请求，在请求头中的Authorization添加Bearer token
# get_user_token在auth.py中
# @router.get("/get_token")
# async def get_token(data=Depends(get_user_token)):
#     return data

## 另外一种定义方式：放在url参数中
# http://127.0.0.1:8000/quanxian/get_token?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImphY2siLCJleHAiOjE3NjUyNzM0NTR9.734AJnkqzxpfCxAt6ukx23Iqx0j04MCukdk4Q0BbkoA
# @router.get("/get_token")
# async def get_token(token):
#     data = get_user_token(token)
#     return data


## 验证过期
@router.get("/get_token")
async def get_token(token=Depends(get_user_token)):
    return token


# 查询角色的权限
def get_role_permissions(role_name: list[str]):
    print(role_name)
    permissions = []
    for role in role_name:
        for perm in ROLE_PERMISSIONS[role]:
            permissions.append(perm)
            print(permissions)
    return permissions


# 查询用户的角色
def get_user_permissions(token: str = Depends(get_username)):  # 原：get_user_token
    if token in ALL_USERS:
        return get_role_permissions(ALL_USERS[token])
    return None


def check_user(security_scopes: SecurityScopes, user_permission: str = Depends(get_user_permissions)):
    # 先获取用户权限（前提通过Cookie获取用户名），有用户名就知道角色，知道角色就为他添加权限
    for scope in security_scopes.scopes:
        if scope not in user_permission:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无权限")


@router.get("/upload", dependencies=[Security(check_user, scopes=['upload'])])
async def upload():
    return {"message": "upload权限"}


@router.get("/visit", dependencies=[Security(check_user, scopes=['visit'])])
async def visit():
    return {"visit": "visit权限"}


@router.get("/download", dependencies=[Security(check_user, scopes=['download'])])
async def download():
    return {"message": "download权限"}