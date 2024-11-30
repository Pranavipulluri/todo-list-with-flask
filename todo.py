from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect("todolist.db") as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """)
        con.commit()

@app.route("/")
def index():
    # Fetch all tasks from the database
    with sqlite3.connect("todolist.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    if title.strip():  # Ensure task title is not empty
        with sqlite3.connect("todolist.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, "Incomplete"))
            con.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    with sqlite3.connect("todolist.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        con.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    new_status = request.form["status"]
    with sqlite3.connect("todolist.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        con.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
