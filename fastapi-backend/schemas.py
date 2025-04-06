# schemas.py   #定義資料格式
from pydantic import BaseModel
from typing import Literal, Optional


# 用來描述 "data" 裡面的內容
class NoteData(BaseModel):
    uuid: Optional[str] = None  # 可選：用於 delete / update / patch
    title: Optional[str] = None
    content: Optional[str] = None


# 整個 POST 請求的格式
class NotePayload(BaseModel):
    action: Literal["create", "delete", "update", "patch"]
    data: NoteData

