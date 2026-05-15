from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("todos.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    completed INTEGER DEFAULT 0
)
""")
conn.commit()


@app.get("/")
def home():
    return {"message": "API running"}


@app.get("/todos")
def get_todos():
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()

    todos = []

    for row in rows:
        todos.append({
            "id": row[0],
            "task": row[1],
            "completed": bool(row[2])
        })

    return todos


@app.post("/todos")
def add_todo(item: str):
    cursor.execute(
        "INSERT INTO todos (task, completed) VALUES (?, ?)",
        (item, 0)
    )
    conn.commit()

    return {"message": "added"}


@app.delete("/todos/{id}")
def delete_todo(id: int):
    cursor.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()

    return {"message": "deleted"}


@app.put("/todos/{id}")
def update_todo(id: int, item: str):
    cursor.execute(
        "UPDATE todos SET task = ? WHERE id = ?",
        (item, id)
    )
    conn.commit()

    return {"message": "updated"}


@app.put("/todos/{id}/complete")
def complete_todo(id: int):
    cursor.execute(
        "UPDATE todos SET completed = 1 WHERE id = ?",
        (id,)
    )
    conn.commit()

    return {"message": "completed"}


@app.delete("/todos/completed")
def clear_completed():
    cursor.execute(
        "DELETE FROM todos WHERE completed = 1"
    )
    conn.commit()

    return {"message": "completed tasks deleted"}