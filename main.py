from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


import sqlite3

def get_conn():
    conn = sqlite3.connect("todos.db")   # 会自动创建 todos.db 文件
    conn.row_factory = sqlite3.Row       # 让查询结果能按列名访问，如 row["title"]
    return conn

# 启动时建表（如果还没有的话）
with get_conn() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done  INTEGER NOT NULL DEFAULT 0
        )
    """)
conn.close()


app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    done: bool = False

class TodoOut(TodoCreate):
    id: int

todos = []
next_id = 1


@app.post("/todos", response_model=TodoOut)
def create_todo(payload: TodoCreate):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO todos (title, done) VALUES (?, ?)",
        (payload.title, int(payload.done))
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return TodoOut(id=new_id, title=payload.title, done=payload.done)

@app.get("/todos")
def list_todos():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM todos").fetchall()
    result = [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]
    conn.close()
    return result


@app.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoCreate):
    conn = get_conn()
    try:
        cur = conn.execute(
            "UPDATE todos SET title = ?, done = ? WHERE id = ?",
            (payload.title, int(payload.done), todo_id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="待办不存在")
        conn.commit()
        return TodoOut(id=todo_id, title=payload.title, done=payload.done)
    finally:
        conn.close()


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_conn()
    try:
        cur = conn.execute(
            "DELETE FROM todos WHERE id = ?",
            (todo_id,)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="待办不存在")
        conn.commit()
        return {"message": "已删除"}
    finally:
        conn.close()