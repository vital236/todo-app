import sqlite3
from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
import os

app = Flask(__name__)
app.secret_key = "dev"

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    if request.method == "POST":
        task = request.form.get("task")

        if task:
            conn.execute(
                "INSERT INTO tasks (content, completed) VALUES (?, ?)",
                (task, 0)
            )
            conn.commit()
            flash("Задача добавлена ✔️")

        return redirect("/")

    filter_type = request.args.get("filter", "all")

    if filter_type == "active":
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE completed = 0"
        ).fetchall()

    elif filter_type == "done":
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE completed = 1"
        ).fetchall()

    else:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks, filter_type=filter_type)



@app.route("/delete/<int:task_id>")
def delete(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    conn = get_db_connection()

    task = conn.execute(
        "SELECT completed FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    new_status = 0 if task["completed"] == 1 else 1

    conn.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (new_status, task_id)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/clear_done")
def clear_done():
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
