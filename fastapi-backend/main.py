from fastapi import FastAPI, HTTPException, Body, Query
from db import get_connection
from schemas import NotePayload
import uuid

app = FastAPI()


# ✅ [GET] 讀取資料 -------------------------------------------------------------------
@app.get("/notes")
def read_notes(uuid: str | None = Query(default=None)):
    """
    - 不帶 uuid：回傳全部筆記
    - 帶 uuid：回傳單筆資料
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if uuid:
            cursor.execute("SELECT uuid, title, content FROM notes WHERE uuid = %s", (uuid,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Note not found")
            return {
                "uuid": result[0],
                "title": result[1],
                "content": result[2]
            }
        else:
            cursor.execute("SELECT uuid, title, content FROM notes")
            results = cursor.fetchall()
            return {
                "notes": [
                    {"uuid": row[0], "title": row[1], "content": row[2]}
                    for row in results
                ]
            }
    finally:
        cursor.close()
        conn.close()


# ✅ [POST] 建立 / 刪除 / 更新 / 修改資料 ---------------------------------------------
@app.post("/notes")
def modify_notes(payload: NotePayload):
    """
    根據 payload 中的 action 執行對應 CRUD：
    - create: 新增
    - delete: 刪除
    - update: 整筆更新
    - patch: 局部更新
    """
    action = payload.get("action")
    data = payload.get("data", {})

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if action == "create":
            note_uuid = str(uuid.uuid4())
            sql = "INSERT INTO notes (uuid, title, content) VALUES (%s, %s, %s)"
            cursor.execute(sql, (note_uuid, data.get("title"), data.get("content")))
            conn.commit()
            return {"message": "Note created", "uuid": note_uuid}

        elif action == "delete":
            cursor.execute("DELETE FROM notes WHERE uuid = %s", (data.get("uuid"),))
            conn.commit()
            return {"message": "Note deleted"}

        elif action == "update":
            cursor.execute(
                "UPDATE notes SET title = %s, content = %s WHERE uuid = %s",
                (data.get("title"), data.get("content"), data.get("uuid"))
            )
            conn.commit()
            return {"message": "Note updated"}

        elif action == "patch":
            fields = []
            values = []

            if data.get("title"):
                fields.append("title=%s")
                values.append(data.get("title"))
            if data.get("content"):
                fields.append("content=%s")
                values.append(data.get("content"))

            if not fields:
                raise HTTPException(status_code=400, detail="No patch data provided")

            values.append(data.get("uuid"))
            sql = f"UPDATE notes SET {', '.join(fields)} WHERE uuid = %s"
            cursor.execute(sql, values)
            conn.commit()
            return {"message": "Note patched"}

        else:
            raise HTTPException(status_code=400, detail="Invalid action")

    finally:
        cursor.close()
        conn.close()
