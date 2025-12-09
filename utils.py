# 该页面用于分担main中的“工具函数”
import hashlib
import uuid



FILE_PATH = "files"

# 异步保存
async def save_files(file):
    path = FILE_PATH
    res = await file.read()
    unique_name = hashlib.md5(str(uuid.uuid4()).encode("utf-8")).hexdigest()[:8]
    file_name = f"{unique_name}.{file.filename.rsplit('.', 1)[-1]}"
    full_file = f"{path}/{file_name}"
    with open(full_file, "wb") as f:
        f.write(res)
    return full_file