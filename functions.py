import json

FILEPATH = "todos.json"

def get_todos():
    try:
        with open(FILEPATH, "r") as file:
            return json.load(file)
    except:
        return []

def write_todos(todos):
    with open(FILEPATH, "w") as file:
        json.dump(todos, file, indent=4)