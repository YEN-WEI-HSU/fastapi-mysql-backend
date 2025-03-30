# schemas.py   #定義資料格式
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class Note(NoteBase):
    id: int

    class Config:
        orm_mode = True

