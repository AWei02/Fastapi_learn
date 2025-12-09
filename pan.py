import os
import hashlib
import uuid
from fastapi import APIRouter, UploadFile, Request, Response
from fastapi.responses import FileResponse


from utils import save_files



router = APIRouter()

FILE_PATH = "files"


@router.get("/")
async def root_api():
    return {"message": "API"}


# 获取请求体里上传的文件（用内存缓存，如果太大，超过阈值会写入磁盘）
# summary="上传文件"是swaggerUI中的摘要，方便查看
@router.post("/uploadfile/", summary="上传文件")
async def create_upload_file(file: UploadFile):
    file_local = await save_files(file)  # 调用异步方法用await
    return {"filename": file.filename,
            "content_type": file.content_type,  # 文件类型
            }


# # 异步保存，放 utils 中调用
# async def save_files(file):
#     path = FILE_PATH
#     res = await file.read()
#     unique_name = hashlib.md5(str(uuid.uuid4()).encode("utf-8")).hexdigest()[:8]
#     file_name = f"{unique_name}.{file.filename.rsplit('.', 1)[-1]}"
#     full_file = f"{path}/{file_name}"
#     with open(full_file, "wb") as f:
#         f.write(res)
#     return full_file



@router.get("/downloadfile/", summary="下载文件")
async def download_file_list(request: Request):
    data = {
        "index": '8e30145f',
    }
    return request.app.state.templates.TemplateResponse(name="downloadpage.html", context=data, request=request)


# 通过路径下载文件
@router.get("/downloadfile/{index}")
async def download_excel_file(index: str):
    file_path = os.path.join(FILE_PATH, f"{index}.xlsx")
    return FileResponse(
        path=file_path,
        filename="对文件重新命名.xlsx",  # 如果没有重命名的话，删除缓存即可
        media_type="application/octet-stream"  # 可要可不要
        # media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # 可要可不要
    )


# 设置cookie
@router.get("/set")
async def set_cookie(resp: Response):
    resp.set_cookie(key="pan_token", value="123", expires=60,)
    return {"message": "set"}
