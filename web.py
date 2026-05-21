import streamlit as st
import pandas as pd
import uuid
from datetime import date

import functions  # must handle read/write from file or DB

# =========================
# 🔹 INITIAL LOAD OF TODOS
# =========================
todos = functions.get_todos()  # expected: list of dicts

# =========================
# 🔹 SESSION STATE INIT
# =========================
if "new_todo" not in st.session_state:
    st.session_state["new_todo"] = ""

if "selected_todo" not in st.session_state:
    st.session_state["selected_todo"] = None

if "priority" not in st.session_state:
    st.session_state["priority"] = "Low"

if "due_date" not in st.session_state:
    st.session_state["due_date"] = date.today()

if "completed_count" not in st.session_state:
    st.session_state["completed_count"] = 0


# =========================
# 🔹 ADD TODO FUNCTION
# =========================
def add_todo():
    """Add a new todo to the list"""

    new_task = st.session_state["new_todo"]

    if new_task.strip() == "":
        return

    todo = {
        "id": str(uuid.uuid4()),  # unique ID for each task
        "task": new_task,
        "priority": st.session_state["priority"],
        "due_date": str(st.session_state["due_date"]),
        "completed": False
    }

    todos.append(todo)
    functions.write_todos(todos)

    # reset input
    st.session_state["new_todo"] = ""


# =========================
# 🔹 UPDATE TODO FUNCTION
# =========================
def update_todo():
    """Update selected todo"""

    if st.session_state["selected_todo"] is None:
        return

    todo_id = st.session_state["selected_todo"]

    for todo in todos:
        if todo["id"] == todo_id:
            todo["task"] = st.session_state["new_todo"]
            todo["priority"] = st.session_state["priority"]
            todo["due_date"] = str(st.session_state["due_date"])

    functions.write_todos(todos)

    # reset
    st.session_state["new_todo"] = ""
    st.session_state["selected_todo"] = None


# =========================
# 🔹 COMPLETE TODO FUNCTION
# =========================
def delete_task(todo_id):
    """Delete task and increase progress"""

    updated_todos = [
        todo for todo in todos
        if todo["id"] != todo_id
    ]

    # increase completed count
    st.session_state["completed_count"] += 1

    functions.write_todos(updated_todos)

# =========================
# 🔹 STATS CALCULATION
# =========================
# Total tasks originally created
total_tasks = len(todos) + st.session_state["completed_count"]

# Tasks deleted/completed
completed_tasks = st.session_state["completed_count"]

# Remaining tasks
pending_tasks = len(todos)

# Progress calculation
progress = (
    completed_tasks / total_tasks
    if total_tasks > 0 else 0
)


# =========================
# 🔹 TITLE
# =========================
st.title("📋 Smart Task Management App")
st.subheader("Manage your tasks efficiently")


# =========================
# 🔹 DASHBOARD (PROGRESS + CHART)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.write("📊 Task Progress")
    st.progress(progress)
    st.write(f"{int(progress * 100)}% Completed")

with col2:
    st.write("📈 Task Analytics")

    chart_data = pd.DataFrame({
        "Status": ["Completed", "Pending"],
        "Count": [completed_tasks, pending_tasks]
    })

    st.bar_chart(chart_data.set_index("Status"))


# =========================
# 🔹 DISPLAY TASKS
# =========================
st.write("---")
st.write(f"### Total Tasks: {total_tasks}")


for todo in todos:

    todo_id = todo["id"]
    task = todo["task"]
    priority = todo["priority"]
    due_date = todo["due_date"]
    completed = todo["completed"]

    # format display text
    display_text = f"{priority} | {task} (Due: {due_date})"

    col1, col2 = st.columns([5, 1])

    # =========================
    # CHECKBOX (COMPLETE TASK)
    # =========================
    with col1:
        checked = st.checkbox(
            display_text,
            value=False,
            key=f"todo_{todo_id}"
        )

        # if checkbox selected → delete task
        if checked:
            delete_task(todo_id)
            st.rerun()

    # =========================
    # EDIT BUTTON
    # =========================
    with col2:
        if st.button("✏️ Edit", key=f"edit_{todo_id}"):

            st.session_state["new_todo"] = task
            st.session_state["selected_todo"] = todo_id
            st.session_state["priority"] = priority
            st.session_state["due_date"] = date.fromisoformat(due_date)


# =========================
# 🔹 INPUT SECTION (ADD / EDIT)
# =========================

st.write("---")
st.write("### ➕ Add / Edit Task")

# priority selector
st.session_state["priority"] = st.selectbox(
    "Priority",
    ["High", "Medium", "Low"]
)

# due date selector
st.session_state["due_date"] = st.date_input("Due Date")

# task input
st.text_input(
    "Task",
    placeholder="Enter your task...",
    key="new_todo"
)

col1, col2 = st.columns(2)

with col1:
    st.button("➕ Add Todo", on_click=add_todo)

with col2:
    st.button("💾 Update Todo", on_click=update_todo)