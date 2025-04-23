# schemas.py   #定義資料格式
from pydantic import BaseModel                #引入 Pydantic 的基礎類別 `BaseModel`
from typing import Literal, Optional


# 用來描述 "data" 裡面的內容  #資料區塊（data 欄位）
class NoteData(BaseModel):
    uuid: Optional[str] = None  # 可選：用於 delete / update / patch    # 欄位名稱: 型別 = 預設值
    title: Optional[str] = None
    content: Optional[str] = None


# 整個 POST 請求的格式
class NotePayload(BaseModel):
    action: Literal["create", "delete", "update", "patch"]
    data: NoteData

