import time
from fastapi import FastAPI, Request, Response
# import logging


# logger = logging.getLogger("uvicorn.access")
# logger.disabled = True  # 关闭日志显示


## 通过函数实现中间件
# def my_logger(message: str):
#     print(message)

# def tai_middleware(app: FastAPI):
#     @app.middleware('http')
#     async def count_time(request:Request, call_next):
#         start_time = time.time()
#         response = await call_next(request)
#         response_time = time.time() - start_time
#         print(f"请求处理时间：{response_time}")
#         return response
    
#     @app.middleware('http')
#     async def tai_logging(request:Request, call_next):
#         message = f"{request.client.host}:{request.client.port} {request.method} {request.url.path}"
#         my_logger(message)
#         response = await call_next(request)

#         return response


## 通过类实现中间件
# 限制访问速率>5秒
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.request_records: dict[str, float] = defaultdict(float)  # defaultdict每当有不存在的键值对，会新建
        # 存储在自身的堆中

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host  # 获取客户端IP
        current_time = time.time()  # fastapi接收客户端的请求时间
        
        if current_time - self.request_records[ip] < 5:
            return Response(content="超过访问限制", status_code=429)
        
        response = await call_next(request)
        self.request_records[ip] = current_time  # 成功响应，将请求IP和请求时间保存在字典里

        return response
    
        
def tai_middleware(app: FastAPI):
    # 加载中间件
    app.add_middleware(RateLimitMiddleware)

    ## 中间件解决跨域问题
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(CORSMiddleware,
                        allow_origins=["*"],
                        allow_methods=["*"],
                        allow_headers=["*"],
                        allow_credentials=False,
                       )




