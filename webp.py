from streamlit import columns, text_input, date_input, title, rerun, button, subheader, selectbox, checkbox, progress, \
    bar_chart, session_state, write
import pandas as pd
import uuid
from datetime import date

import database  # must handle read/write from file or DB

# =========================
# 🔹 INITIAL LOAD OF TODOS
# =========================
todos = database.get_tasks()
# =========================
# 🔹 SESSION STATE INIT
# =========================
if "new_todo" not in session_state:
    session_state["new_todo"] = ""

if "selected_todo" not in session_state:
    session_state["selected_todo"] = None

if "priority" not in session_state:
    session_state["priority"] = "Low"

if "due_date" not in session_state:
    session_state["due_date"] = date.today()

if "completed_count" not in session_state:
    session_state["completed_count"] = 0


# =========================
# 🔹 ADD TODO FUNCTION
# =========================
def add_todo():
    """Add a new todo to the list"""

    new_task = session_state["new_todo"]

    if new_task.strip() == "":
        return

    todo = {
        "id": str(uuid.uuid4()),  # unique ID for each task
        "task": new_task,
        "priority": session_state["priority"],
        "due_date": str(session_state["due_date"]),
        "status": "Pending"
    }

    database.add_task(todo)

    # reset input
    session_state["new_todo"] = ""


# =========================
# 🔹 UPDATE TODO FUNCTION
# =========================
def update_todo():
    """Update selected todo"""

    if session_state["selected_todo"] is None:
        return

    todo_id = session_state["selected_todo"]

    for todo in todos:
        if todo["id"] == todo_id:
            todo["task"] = session_state["new_todo"]
            todo["priority"] = session_state["priority"]
            todo["due_date"] = str(session_state["due_date"])

    database.update_task(
        todo_id,
        session_state["new_todo"],
        session_state["priority"],
        str(session_state["due_date"])
    )

    # reset
    session_state["new_todo"] = ""
    session_state["selected_todo"] = None


# =========================
# 🔹 COMPLETE TODO FUNCTION
# =========================
def complete_task(todo_id):
    database.update_task_status(todo_id)

# =========================
# =========================
# 🔹 STATS CALCULATION
# =========================

total_tasks = len(todos)

completed_tasks = sum(
    1 for t in todos
    if t["status"] == "Completed"
)

pending_tasks = sum(
    1 for t in todos
    if t["status"] == "Pending"
)

progress_value = (
    completed_tasks / total_tasks
    if total_tasks > 0 else 0
)


# =========================
# 🔹 TITLE
# =========================
title("📋 Smart Task Management App")
subheader("Manage your tasks efficiently")


# =========================
# 🔹 DASHBOARD (PROGRESS + CHART)
# =========================
col1, col2 = columns(2)

with col1:
    write("📊 Task Progress")
    progress(progress_value)
    write(f"{int(progress_value * 100)}% Completed")

with col2:
    write("📈 Task Analytics")

    chart_data = pd.DataFrame({
        "Status": ["Completed", "Pending"],
        "Count": [completed_tasks, pending_tasks]
    })

    bar_chart(chart_data.set_index("Status"))


# =========================
# 🔹 DISPLAY TASKS
# =========================
write("---")
write(f"### Total Tasks: {total_tasks}")


for todo in todos:

    todo_id = todo["id"]
    task = todo["task"]
    priority = todo["priority"]
    due_date = todo["due_date"]
    status = todo["status"]

    # format display text
    display_text = (
        f"{priority} | {task} "
        f"(Due: {due_date}) | Status: {status}"
    )

    col1, col2 = columns([5, 1])

    # =========================
    # CHECKBOX (COMPLETE TASK)
    # =========================
    with col1:
        checked = checkbox(
            display_text,
            value=False,
            key=f"todo_{todo_id}"
        )

        # if user checks box → mark complete
        if checked and status == "Pending":
            complete_task(todo_id)
            rerun()

    # =========================
    # EDIT BUTTON
    # =========================
    with col2:
        if button("✏️ Edit", key=f"edit_{todo_id}"):

            session_state["new_todo"] = task
            session_state["selected_todo"] = todo_id
            session_state["priority"] = priority
            session_state["due_date"] = date.fromisoformat(due_date)


# =========================
# 🔹 INPUT SECTION (ADD / EDIT)
# =========================

write("---")
write("### ➕ Add / Edit Task")

# priority selector
session_state["priority"] = selectbox(
    "Priority",
    ["High", "Medium", "Low"]
)

# due date selector
session_state["due_date"] = date_input("Due Date")

# task input
text_input(
    "Task",
    placeholder="Enter your task...",
    key="new_todo"
)

col1, col2 = columns(2)

with col1:
    button("➕ Add Todo", on_click=add_todo)

with col2:
    button("💾 Update Todo", on_click=update_todo)