from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB connection
def get_db():
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    return conn, cursor


# INIT DB (run once safely)
conn, cursor = get_db()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    completed INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()


# HOME
@app.get("/")
def home():
    return {"message": "API running"}


# GET TODOS
@app.get("/todos")
def get_todos():
    conn, cursor = get_db()

    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "task": row[1],
            "completed": bool(row[2])
        }
        for row in rows
    ]


# ADD TODO
@app.post("/todos")
def add_todo(item: str):
    conn, cursor = get_db()

    cursor.execute(
        "INSERT INTO todos (task, completed) VALUES (?, ?)",
        (item, 0)
    )

    conn.commit()
    conn.close()

    return {"message": "added"}


# TOGGLE COMPLETE
@app.put("/todos/{id}/complete")
def toggle_complete(id: int):
    conn, cursor = get_db()

    cursor.execute("SELECT completed FROM todos WHERE id=?", (id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"error": "todo not found"}

    new_value = 0 if row[0] == 1 else 1

    cursor.execute(
        "UPDATE todos SET completed=? WHERE id=?",
        (new_value, id)
    )

    conn.commit()
    conn.close()

    return {"message": "updated"}


# DELETE TODO
@app.delete("/todos/{id}")
def delete_todo(id: int):
    conn, cursor = get_db()

    cursor.execute("DELETE FROM todos WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return {"message": "deleted"}


# EDIT TODO
@app.put("/todos/{id}")
def update_todo(id: int, item: str):
    conn, cursor = get_db()

    cursor.execute(
        "UPDATE todos SET task=? WHERE id=?",
        (item, id)
    )

    conn.commit()
    conn.close()

    return {"message": "updated"}


# CLEAR COMPLETED
@app.delete("/todos/completed")
def clear_completed():
    conn, cursor = get_db()

    cursor.execute("DELETE FROM todos WHERE completed=1")

    conn.commit()
    conn.close()

    return {"message": "completed cleared"}