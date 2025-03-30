#進入pipenv虛擬環境指令: pipenv shell

# main.py
from fastapi import FastAPI, HTTPException
from db import get_connection
from schemas import NoteCreate, NoteUpdate, Note

app = FastAPI()

# 測試根目錄
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI 🎉"}

# 取得所有筆記
@app.get("/notes")
def get_notes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM notes")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    notes = []
    for row in results:
        notes.append({"id": row[0], "title": row[1], "content": row[2]})
    return {"notes": notes}

# 取得單一筆記
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM notes WHERE id = %s", (note_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Note not found")

    return {"id": result[0], "title": result[1], "content": result[2]}

# 新增筆記
@app.post("/notes")
def create_note(note: NoteCreate):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO notes (title, content) VALUES (%s, %s)"
    cursor.execute(sql, (note.title, note.content))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Note created successfully"}

# 更新整筆筆記
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title=%s, content=%s WHERE id=%s", (note.title, note.content, note_id))
    conn.commit()
    updated_rows = cursor.rowcount
    cursor.close()
    conn.close()

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note updated successfully"}

# 局部更新（例如只更新 title 或 content）
@app.patch("/notes/{note_id}")
def patch_note(note_id: int, note: NoteUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    update_fields = []
    values = []

    if note.title is not None:
        update_fields.append("title = %s")
        values.append(note.title)
    if note.content is not None:
        update_fields.append("content = %s")
        values.append(note.content)

    if not update_fields:
        raise HTTPException(status_code=400, detail="No data provided for update")

    values.append(note_id)
    sql = f"UPDATE notes SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(sql, values)
    conn.commit()
    updated_rows = cursor.rowcount
    cursor.close()
    conn.close()

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note patched successfully"}

# 刪除筆記
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    cursor.close()
    conn.close()

    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}



#  uvicorn main:app --host 0.0.0.0 --port 8000  #啟動伺服器
# 瀏覽器開啟 http://localhost:8000/docs