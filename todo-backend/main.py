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

# DATABASE CONNECTION
conn = sqlite3.connect(
    "todos.db",
    check_same_thread=False
)

cursor = conn.cursor()

# TABLE CREATE
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    completed INTEGER DEFAULT 0
)
""")

conn.commit()


# HOME ROUTE
@app.get("/")
def home():
    return {"message": "API running"}


# GET TODOS
@app.get("/todos")
def get_todos():
    cursor.execute("SELECT * FROM todos")
    return cursor.fetchall()


# ADD TODO
@app.post("/todos")
def add_todo(item: str):
    cursor.execute(
        "INSERT INTO todos (task) VALUES (?)",
        (item,)
    )

    conn.commit()

    return {"message": "added"}


# CLEAR COMPLETED
# IMPORTANT:
# This route must stay ABOVE /todos/{id}

@app.delete("/todos/completed")
def clear_completed():

    cursor.execute(
        "DELETE FROM todos WHERE completed = 1"
    )

    conn.commit()

    return {"message": "completed todos deleted"}


# DELETE TODO
@app.delete("/todos/{id}")
def delete_todo(id: int):

    cursor.execute(
        "DELETE FROM todos WHERE id = ?",
        (id,)
    )

    conn.commit()

    return {"message": "deleted"}


# EDIT TODO
@app.put("/todos/{id}")
def update_todo(id: int, item: str):

    cursor.execute(
        "UPDATE todos SET task = ? WHERE id = ?",
        (item, id)
    )

    conn.commit()

    return {"message": "updated"}


# TOGGLE COMPLETE
@app.put("/todos/{id}/complete")
def toggle_complete(id: int):

    cursor.execute(
        "SELECT completed FROM todos WHERE id = ?",
        (id,)
    )

    current = cursor.fetchone()[0]

    new_value = 0 if current == 1 else 1

    cursor.execute(
        "UPDATE todos SET completed = ? WHERE id = ?",
        (new_value, id)
    )

    conn.commit()

    return {"message": "toggled"}