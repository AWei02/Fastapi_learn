from fastapi import FastAPI


grand_son_app = FastAPI()  # 定义子应用


@grand_son_app.get("/")
async def root():
    return {"message": "我是子应用的子应用"}