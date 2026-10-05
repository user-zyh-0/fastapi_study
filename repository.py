import sqlite3


def get_conn():
    conn = sqlite3.connect("todos.db")  # 会自动创建 todos.db 文件
    conn.row_factory = sqlite3.Row  # 让查询结果能按列名访问，如 row["title"]
    return conn


def init_db():
    conn = get_conn()
    try:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS todos
                     (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         done INTEGER NOT NULL DEFAULT 0
                     )
                     """)
        conn.commit()
    finally:
        conn.close()


def create_todo(title, done):
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO todos (title, done) VALUES (?, ?)",
            (title, int(done))
        )
        conn.commit()
        new_id = cur.lastrowid
        return dict(id=new_id, title=title, done=bool(done))
    finally:
        conn.close()


def list_todos():
    conn = get_conn()
    try:
        rows = conn.execute("SELECT * FROM todos").fetchall()
        result = [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]
        return result
    finally:
        conn.close()


def get_todo(todo_id):
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM todos WHERE id = ?",
            (todo_id,)
        ).fetchone()
        if row is None:
            return False
        result = {"id": row["id"], "title": row["title"], "done": bool(row["done"])}
        return result
    finally:
        conn.close()


def update_todo(todo_id, title, done):
    conn = get_conn()
    try:
        cur = conn.execute(
            "UPDATE todos SET title = ?, done = ? WHERE id = ?",
            (title, int(done), todo_id)
        )
        if cur.rowcount == 0:
            return False
        conn.commit()
        return dict(id=todo_id, title=title, done=bool(done))
    finally:
        conn.close()


def delete_todo(todo_id):
    conn = get_conn()
    try:
        cur = conn.execute(
            "DELETE FROM todos WHERE id = ?",
            (todo_id,)
        )
        if cur.rowcount == 0:
            return False
        conn.commit()
        return True
    finally:
        conn.close()
