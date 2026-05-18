# Line by Line Explanation of My To‑Do App (Very Easy Version)

## 1) Importing Required Modules

```python
import functions
```
**Meaning:**
This imports another Python file called `functions.py`.

Think of it like asking your friend for help.

Your app says:
> “Hey functions.py, help me save and read my to‑do tasks.”

This file is used for:
- Reading saved tasks
- Saving new tasks
- Updating tasks

---

```python
import PySimpleGUI as sg
```
**Meaning:**
This imports a special tool called **PySimpleGUI**.

Think of it like a LEGO box for building windows, buttons, textboxes, and lists.

Without this, your app cannot make a GUI window.

`as sg` means:

Instead of writing:

```python
PySimpleGUI.Text()
```

we can simply write:

```python
sg.Text()
```

This saves typing time.

---

```python
import time
```
**Meaning:**
This imports the `time` module.

We use it to show the live clock.

Without this, your app cannot show:

```text
May 18, 2026 10:30:45
```

---

## 2) GUI Theme

```python
sg.theme("Black")
```

**Meaning:**
This changes the app color theme.

You are telling Python:

> “Make my app look black.”

Without this line, the app uses the default theme.

---

## 3) Creating Clock

```python
clock = sg.Text('', key='clock')
```

**Meaning:**
This creates an empty text area.

Later, we will put time inside it.

At first:

```text
(empty)
```

Later:

```text
May 18, 2026 10:30:45
```

### What is `key='clock'`?

A key is like a **name tag**.

Imagine your classroom:

Everyone has a name.

Same here.

We give this text area the name:

```python
clock
```

So later we can update it.

---

## 4) Label Text

```python
label = sg.Text("Type in a to-do")
```

**Meaning:**
This creates a text label.

It simply shows:

```text
Type in a to-do
```

It helps the user understand what to do.

---

## 5) Input Box

```python
input_box = sg.InputText(
    tooltip="Enter todo",
    key="todo",
    size=(60, 2)
)
```

**Meaning:**
This creates a textbox.

The user types tasks here.

Example:

```text
Study Python
```

### `tooltip="Enter todo"`

When mouse hovers:

A tiny message appears:

```text
Enter todo
```

Like a helpful hint.

### `key="todo"`

This gives the textbox a name.

Now Python can read what user typed.

Example:

```python
values['todo']
```

means:

> “Tell me what the user typed.”

### `size=(60, 2)`

This changes textbox size.

- 60 = width
- 2 = height

---

## 6) Buttons

```python
add_button = sg.Button("Add", size=(12, 2))
```

Creates Add button.

When clicked:

New task gets added.

---

```python
edit_button = sg.Button("Edit", size=(12, 2))
```

Creates Edit button.

Used to change a task.

Example:

Before:

```text
Study SQL
```

After edit:

```text
Study Python
```

---

```python
complete_button = sg.Button("Complete", size=(12, 2))
```

Creates Complete button.

This removes finished tasks.

Example:

Before:

```text
Buy milk
```

After clicking Complete:

❌ Task gone.

---

```python
exit_button = sg.Button("Exit", size=(12, 2))
```

Creates Exit button.

Used for closing the app.

---

## 7) Todo List Box

```python
list_box = sg.Listbox(
    values=functions.get_todos(),
    key='todos',
    enable_events=True,
    size=[45, 11]
)
```

**Meaning:**
This creates a big box where tasks are shown.

Example:

```text
Study Python
Buy Milk
Learn React
```

### `functions.get_todos()`

This reads saved tasks from file.

Imagine opening a notebook and reading old homework.

Same thing.

### `key='todos'`

Gives the list a name.

Now Python knows:

> “This is my todo list.”

### `enable_events=True`

Means:

If user clicks task:

Python notices it.

Example:

User clicks:

```text
Study Python
```

Textbox automatically shows it.

### `size=[45,11]`

Changes size of todo list.

---

## 8) Window Design

```python
window = sg.Window(
    'My To-Do App',
```

This creates app window.

Window title becomes:

```text
My To‑Do App
```

---

## 9) Layout

```python
layout=[
    [clock],
    [label],
    [input_box],
```

This decides where things appear.

Like arranging toys in a room.

Row 1:

Clock

Row 2:

Label

Row 3:

Textbox

---

```python
[list_box,
 sg.Column([
     [add_button],
     [edit_button],
     [complete_button],
     [exit_button]
 ])
]
```

This puts buttons vertically beside list.

Like this:

```text
+-------------+   +--------+
| Todo List   |   | Add    |
|             |   | Edit   |
|             |   | Complete |
|             |   | Exit   |
+-------------+   +--------+
```

---

```python
font=('Helvetica', 20)
```

Makes text look bigger.

20 means font size.

---

## 10) Main Loop

```python
while True:
```

This means:

> “Keep app running forever.”

Without this:

App opens and closes immediately.

---

## 11) Reading User Action

```python
event, values = window.read(timeout=200)
```

This is the HEART of the app ❤️

Python checks:

- Did user click button?
- Did user type something?
- Did user select todo?

### `event`

Stores what happened.

Example:

```python
event = "Add"
```

means Add button clicked.

### `values`

Stores user data.

Example:

```python
values = {
    'todo': 'Study Python'
}
```

means user typed:

```text
Study Python
```

---

## 12) Live Clock Update

```python
window['clock'].update(
    value=time.strftime("%b %d, %Y %H:%M:%S")
)
```

Updates clock every second.

Example:

```text
May 18, 2026 10:35:44
```

---

## 13) Match Case

```python
match event:
```

Means:

> “Check what user clicked.”

---

## 14) Add Button Logic

```python
case "Add":
```

If Add button clicked:

Run this code.

```python
todos = functions.get_todos()
```

Read old todos.

---

```python
new_todo = values['todo'] + "\n"
```

Take user text.

Example:

```text
Study Python
```

`\n` means next line.

---

```python
todos.append(new_todo)
```

Adds task into list.

---

```python
functions.write_todos(todos)
```

Save tasks into file.

---

```python
window['todos'].update(values=todos)
```

Refresh list instantly.

---

## 15) Edit Button Logic

```python
todo_to_edit = values['todos'][0]
```

Gets selected todo.

Example:

```text
Study SQL
```

---

```python
new_todo = values['todo'] + "\n"
```

Gets updated text.

Example:

```text
Study Python
```

---

```python
index = todos.index(todo_to_edit)
```

Finds where old task exists.

---

```python
todos[index] = new_todo
```

Replaces old task.

---

## 16) Complete Button

```python
todos.remove(todo_to_complete)
```

Removes selected task.

Like crossing homework off your notebook.

---

## 17) Popup Message

```python
sg.popup("Please select an item first.")
```

Shows warning popup.

If user clicks Edit/Complete without choosing task.

---

## 18) Clicking Todo

```python
case 'todos':
```

When user clicks task:

Textbox automatically fills.

Example:

User clicks:

```text
Learn React
```

Textbox becomes:

```text
Learn React
```

---

## 19) Exit

```python
case "Exit":
    break
```

Break means:

> Stop app.

---

## 20) Closing Window

```python
window.close()
```

Closes app properly.

Like turning off TV after watching.

