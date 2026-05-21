import sqlite3


# Connect to database
connection = sqlite3.connect("todo.db")

# Create cursor
cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    priority TEXT,
    due_date TEXT,
    status TEXT
)
""")

# Save changes
connection.commit()

# Close connection
connection.close()