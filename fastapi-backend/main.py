from fastapi import FastAPI, HTTPException, Query
from db import get_connection
from schemas import NotePayload
import uuid

app = FastAPI()


# ✅ [GET] 讀取資料 -------------------------------------------------------------------
@app.get("/notes")
def read_notes(uuid: str | None = Query(default=None)):
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


# ✅ [POST] 根據 action 處理 create / delete / update / patch ------------------------
@app.post("/notes")
def modify_notes(payload: NotePayload):
    action = payload.action
    data = payload.data

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if action == "create":
            note_uuid = str(uuid.uuid4())
            sql = "INSERT INTO notes (uuid, title, content) VALUES (%s, %s, %s)"
            cursor.execute(sql, (note_uuid, data.title, data.content))
            conn.commit()
            return {"message": "Note created", "uuid": note_uuid}

        elif action == "delete":
            cursor.execute("DELETE FROM notes WHERE uuid = %s", (data.uuid,))
            conn.commit()
            return {"message": "Note deleted"}

        elif action == "update":
            cursor.execute(
                "UPDATE notes SET title = %s, content = %s WHERE uuid = %s",
                (data.title, data.content, data.uuid)
            )
            conn.commit()
            return {"message": "Note updated"}

        elif action == "patch":
            fields = []
            values = []

            if data.title:
                fields.append("title = %s")
                values.append(data.title)
            if data.content:
                fields.append("content = %s")
                values.append(data.content)

            if not fields:
                raise HTTPException(status_code=400, detail="No patch data provided")

            values.append(data.uuid)
            sql = f"UPDATE notes SET {', '.join(fields)} WHERE uuid = %s"
            cursor.execute(sql, values)
            conn.commit()
            return {"message": "Note patched"}

        else:
            raise HTTPException(status_code=400, detail="Invalid action")

    finally:
        cursor.close()
        conn.close()
