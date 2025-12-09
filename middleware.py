from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "中间键"}


@router.middleware("http")
async def only_for_request(request: Request, call_next):
    print(f"获取到了请求路径")
    response = await call_next(request)
    return request