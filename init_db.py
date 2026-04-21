import sqlite3

connection = sqlite3.connect("database.db")

with connection:
    connection.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        );
    """)

print("Database created!")
