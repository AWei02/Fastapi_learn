## 运行命令
# ipconfig
# fastapi dev main.py
# fastapi dev main.py --host 0.0.0.0 --port 8000
# uvicorn main:app
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# UploadFile模块在pan.py中有示例
# 注意：一个main就可以写明白，但单文件太臃肿了，所以把路由都放router中，方法函数都放utils中
# pip freeze > requirements.txt
# 如果requirements文件中有包更新了，修改requirements文件后执行pip install -r requirements.txt --upgrade


# 引入python内嵌模块
import sys
import time
from contextlib import asynccontextmanager  # 用于声明周期
# from functools import lru_cache  # 内建缓存（删除最近最少使用策略），仅适用于少量常量配置。不适用于可变参数、异步函数
import hashlib
import dbm  # python内建键值对(key-value)数据库，符合sqlite的存储逻辑，加.db后缀就能看

from enum import Enum
from typing import Annotated  # 元数据声明：强烈推荐这个方法定义Path, Query
# 路径变量用Path，路径查询参数用Query


# 引入第三方包
from fastapi import FastAPI, Request, Response, status, Path, Query
from fastapi import __version__ as fastapi_version
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
# from starlette.responses import HTMLResponse  # 将html网页作为响应
from fastapi.templating import Jinja2Templates  # html网页变量模板
from pydantic import BaseModel  # python自带类型标注库

from database.redis import redis_connect
from database.mysql import register_mysql

# 引入自己编写的包
from router import routers
from config import config
from tmp.sub import grand_son_app


URL_DB = "url_db.db"  # 不写后缀也能用，但是Navicat不方便读取

@asynccontextmanager
async def tai_init(app: FastAPI):
    print("程序启动...")
    app.state.redis = await redis_connect()
    # 其他启动事件
    # logger_init()  启动日志服务
    # db_init()  连接数据库
    # db_settings()  获取动态配置
    # service_init()  启用第三方服务
    # send_email()  发送邮件给维护者

    async with register_mysql(app):
        print("我是生命周期里的yield")
        yield
    # yield print("生命周期中，等下一次被使用")
    await app.state.redis.close()
    # 其他启动事件
    # logger()
    # db_close()
    # service_close()
    # send_email()
    print("程序关闭...")



app = FastAPI(
    debug=config.DEBUG_MODE,
    lifespan=tai_init,
    docs_url="/docs",  # 默认docs路径地址，改成None就隐藏了,http://127.0.0.1:8000/docs
    redoc_url="/redoc",  # 默认redoc路径地址，改成None就隐藏了,http://127.0.0.1:8000/redoc
    )

son_app = FastAPI()  # 定义子应用
son_app.mount("/grand_son", grand_son_app, name="grand_son")  # 子应用再挂载另一个子应用


app.include_router(routers)
app.mount("/sub", StaticFiles(directory="static"), name="statics")  # 静态文件挂载。通常情况这三个字符串命名应一致
app.mount("/son", son_app, name="son")  # 挂载子应用（doc文档中看不到子应用，可通过http://127.0.0.1:8000/son/docs 独立访问）


@app.get("/server-status", include_in_schema=False)
async def server_status(response: Response, token: str | None = None):
    # include_in_schema=False表示在doc中隐藏该路径
    # Response：可以设置响应头里的信息
    # token为可选参数（有默认值None）
    # 访问http://127.0.0.1:8000/server-status?token=WZN，确认服务器是否正常
    if token == "WZN":
        data = {
            "status": "OK",
            "fastapi_version": fastapi_version,
            "python_version": sys.version_info,
                }
        return data
    else:
        response.status_code = status.HTTP_404_NOT_FOUND  # 设置响应状态码
        return {"detail": "Not found"}


@app.get("/")
async def root():
    return {"message": f"Hello {config.STATIC_DIR}"}


@app.get("/son/")  # 该代码如果在挂载son前，才会生效（谁先出现，就访问谁）
async def root():
    return {"message": "我是顶层app的son路径"}


@son_app.get("/")
async def root():
    return {"message": "我是子应用"}


# 声明路径参数的类型
@app.get("/items/{item_id}", name="item")
async def read_item(item_id: int):
    return {"item_id": item_id}


# @app.get("/post")
# async def post_html():
#     # 将html网页作为响应（被Jinja2Templates替代，通常不使用）
#     # 该网页可以从静态网页中获取资源
#     name = '【变量内容】'
#     data = f'''
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Document</title>
# </head>
# <body>
#     <h6>简单html，这是变量内容:{name}</h6>
# </body>
# </html>
# '''
#     return HTMLResponse(content=data)

# 键值对记录所有路径和对应name，url_for找到name反向解析路径

# templates = Jinja2Templates(directory="templates")  # 以指定目录作为模板资源根路径。实现展示界面和数据的分离（MVC）
app.state.templates = Jinja2Templates(directory="templates")  # 如果多个路由都用到templates的话，推荐这种方法


class Site(BaseModel):
    name: str = "网页标题"

page = {
    "title": "这是一篇文章",
    "body": "这是具体内容",
}


@app.get("/post/{change}")
async def post_html(request: Request, change: int):
    # change路径没有默认值，所以必填
    data = {
        "site": Site(),
        "page": page,
        "id": change,
    }
    # data = lru_test(change)
    # print(lru_test.cache_info())  # 打印缓存信息
    return request.app.state.templates.TemplateResponse(name="post.html", context=data, request=request)


# @lru_cache(maxsize=2)
# def lru_test(change):
#     print("显示本信息，表示没有被缓存")
#     time.sleep(3)
#     data = {
#         "site": Site(),
#         "page": page,
#         "id": change,
#     }
#     print("返回结果前，先睡一下")
#     return data



# 独立变量，仅通过类型来确定，只要符合类型就OK
@app.get("/dlbl/{path_1}/{path_2}")
async def dlbl(request: Request, path_1: int, path_2: Annotated[str | None, Path(title="路径变量2")]):
    data = {
        "site": Site(),
        "page": page,
        "id": path_1,
        "path_1": path_1,
        "path_2": path_2,
    }
    return request.app.state.templates.TemplateResponse(name="post.html", context=data, request=request)


# 预设变量，仅能选择预设的几个变量
class TypeName(str, Enum):
    blog: str = "blog"
    comment: str = "comment"
    page: str = "page"

@app.get("/ysbl/{type_name}/{id}")
async def ysbl(request: Request, 
               type_name: TypeName = Path(title="模块类型", description="可选blog、comment、page"),
               id: int = Path(..., gt=0, lt=2, title="int数值", description=">0且<2"),
               index: float = Query(gt=0, lt=10.5, alias="index别名"),
               ):
    # Path可做类型说明和数据校验
    # ...表示必选项
    # request被传入，是可以不在路径上显示的，非必选
    # http://127.0.0.1:8000/ysbl/blog/1?index=5
    # Path, Query实际上也可以用Annotated进行嵌套
    # alias="index别名"是swaggerUI中的别名，方便查看。
    # 👆且传输时会用?index别名=xxx来接受（方便前端请求，如url中可以用-，python只能用_）
    data = None
    if type_name == TypeName.blog:
        data = f"blog模块"
    if type_name == TypeName.comment:
        data = f"comment模块"
    if type_name == TypeName.page:
        data = f"page模块"
    return {"message": f"Hello 预设变量{data}{id}-{index}"}


# 包含路径变量
@app.get("/bhljbl/{file_path:path}")
async def bhljbl(file_path: str):
    return {"message": f"Hello 包含路径变量，{file_path}"}


# post请求，请求体定义
class PostItem(BaseModel):
    original_url: str

# post请求
@app.post("/short/")
async def short(request: Request, url: PostItem):
    short_url = short_radom(original_str=url.original_url)
    store_short_url(short_url, url.original_url)
    return {"short_url": short_url}

# 短链接重定向
@app.get("/short/{short_key}")
async def short(short_key: str):
    url = get_url_by_key(short_key)
    return RedirectResponse(f'https://{url}')

def get_url_by_key(key: str):
    db = dbm.open(URL_DB, "c")
    # url = db.get(key)  # 这个是二进制，没转码
    url = db[key].decode('utf-8')
    db.close()
    return url

def short_radom(*, original_str: str, length: int = 8):
    # 添加*可以让后默认值的放在后面，FastAPI特供
    random_str = hashlib.md5(original_str.encode()).hexdigest()[:length]
    return random_str

def store_short_url(short_url: str, original_url: str):
    db = dbm.open(URL_DB, "c")
    db[short_url] = original_url.encode("utf-8")
    db.close()


# @app.middleware("http")
# async def only_for_request(request: Request, call_next):
#     print(f"获取到了请求路径")
#     response = await call_next(request)
#     return response


# @app.middleware("http")
# async def only_for_response(request: Request, call_next):
#     response = await call_next(request)
#     print(f"获取到了相应结果"+response.headers["Content-Type"])
#     return response


## 实现中间件
# from middleware import tai_middleware

# tai_middleware(app)