# 该页面用于分担main中的“路由”定义
from fastapi import APIRouter, Depends


from pan import router as pan_router # 更直观的路由
from yilai import router as yilai_router
from quanxian import router as quanxian_router
from database.redis import router as redis_router
from account.router import router as account_router
from mail import router as mail_router


from yilai import check_user

routers = APIRouter()
routers.include_router(pan_router, prefix="/api", tags=["API_test"])  # prefix路由前缀，tag在swaggerUI中会展示
routers.include_router(yilai_router, prefix="/yilai", tags=["依赖_test"], dependencies=[Depends(check_user)])  # 让所有接口都调依赖项
routers.include_router(quanxian_router, prefix="/quanxian", tags=["权限_test"])
routers.include_router(redis_router, prefix="/redis", tags=["缓存_test"])
routers.include_router(account_router, prefix="/account", tags=["注册_test"])
routers.include_router(mail_router, prefix="/mail", tags=["邮件_test"])
