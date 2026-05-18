# Import required modules
import functions               # Custom file to read/write todos
import PySimpleGUI as sg       # GUI library
import time                    # For showing live clock


# ---------------- GUI THEME ----------------
sg.theme("Black")


# ---------------- GUI ELEMENTS ----------------

# Clock text (Initially empty)
clock = sg.Text('', key='clock')

# Label
label = sg.Text("Type in a to-do")

# Input box
input_box = sg.InputText(
    tooltip="Enter todo",
    key="todo",
    size=(60, 2)
)

# Buttons
add_button = sg.Button("Add", size=(12, 2))
edit_button = sg.Button("Edit", size=(12, 2))
complete_button = sg.Button("Complete", size=(12, 2))
exit_button = sg.Button("Exit", size=(12, 2))

# Listbox to show todos
list_box = sg.Listbox(
    values=functions.get_todos(),  # Read todos from file
    key='todos',
    enable_events=True,            # Detect clicking a todo
    size=[45, 11]
)




# ---------------- WINDOW DESIGN ----------------

window = sg.Window(
    'My To-Do App',

    layout=[
        [clock],  # Row 1 → Clock
        [label],  # Row 2 → Label
        [input_box],  # Row 3 → Input box

        [list_box,
         sg.Column([
             [add_button],
             [edit_button],
             [complete_button],
             [exit_button]
         ])
         ]
    ],

    font=('Helvetica', 20)
)


# ---------------- MAIN LOOP ----------------
while True:

    # Read user action every 200 milliseconds
    event, values = window.read(timeout=200)

    # Update live clock
    window["clock"].update(
        value=time.strftime("%b %d, %Y %H:%M:%S")
    )

    # Match user action
    match event:

        # -------- ADD BUTTON --------
        case "Add":

            # Read current todos
            todos = functions.get_todos()

            # Take input text
            new_todo = values['todo'] + "\n"

            # Add todo
            todos.append(new_todo)

            # Save into file
            functions.write_todos(todos)

            # Refresh listbox
            window['todos'].update(values=todos)


        # -------- EDIT BUTTON --------
        case "Edit":

            try:
                # Get selected todo
                todo_to_edit = values['todos'][0]

                # Get updated text
                new_todo = values['todo'] + "\n"

                # Read todos
                todos = functions.get_todos()

                # Find selected todo index
                index = todos.index(todo_to_edit)

                # Replace old todo
                todos[index] = new_todo

                # Save updated todos
                functions.write_todos(todos)

                # Refresh listbox
                window['todos'].update(values=todos)

            except IndexError:
                # Show popup if no todo selected
                sg.popup(
                    "Please select an item first.",
                    font=("Helvetica", 20)
                )


        # -------- COMPLETE BUTTON --------
        case "Complete":

            try:
                # Get selected todo
                todo_to_complete = values['todos'][0]

                # Read todos
                todos = functions.get_todos()

                # Remove selected todo
                todos.remove(todo_to_complete)

                # Save updated todos
                functions.write_todos(todos)

                # Refresh listbox
                window['todos'].update(values=todos)

                # Clear input box
                window['todo'].update(value='')

            except IndexError:
                # Popup if no task selected
                sg.popup(
                    "Please select an item first.",
                    font=("Helvetica", 20)
                )


        # -------- CLICKING A TODO --------
        case 'todos':

            # Show selected todo in textbox
            window['todo'].update(
                value=values['todos'][0]
            )


        # -------- EXIT BUTTON --------
        case "Exit":
            break


        # -------- CLOSE WINDOW (X BUTTON) --------
        case sg.WIN_CLOSED:
            break


# Close app
window.close()