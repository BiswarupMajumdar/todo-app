import sqlite3

# connect database
conn = sqlite3.connect("todo.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id TEXT PRIMARY KEY,
    task TEXT NOT NULL,
    priority TEXT,
    due_date TEXT,
    status TEXT
)
""")

conn.commit()


def add_task(task_data):
    cursor.execute("""
    INSERT INTO todos
    VALUES (?, ?, ?, ?, ?)
    """, (
        task_data["id"],
        task_data["task"],
        task_data["priority"],
        task_data["due_date"],
        task_data["status"]
    ))
    conn.commit()


def get_tasks():
    cursor.execute("SELECT * FROM todos")

    rows = cursor.fetchall()

    todos = []

    for row in rows:
        todos.append({
            "id": row[0],
            "task": row[1],
            "priority": row[2],
            "due_date": row[3],
            "status": row[4]
        })

    return todos


def update_task_status(todo_id):
    cursor.execute("""
    UPDATE todos
    SET status = 'Completed'
    WHERE id = ?
    """, (todo_id,))

    conn.commit()


def update_task(todo_id, task, priority, due_date):
    cursor.execute("""
    UPDATE todos
    SET task=?, priority=?, due_date=?
    WHERE id=?
    """, (task, priority, due_date, todo_id))

    conn.commit()