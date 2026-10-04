from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0)""")

@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    rows = get_db().execute("SELECT * FROM tasks").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error": "title required"}), 400
    with get_db() as db:
        cur = db.execute("INSERT INTO tasks (title) VALUES (?)", (data["title"],))
    return jsonify({"id": cur.lastrowid, "title": data["title"], "done": 0}), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    with get_db() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return jsonify({"error": "task not found"}), 404
        title = data.get("title", row["title"])
        done = int(data.get("done", row["done"]))
        if not title.strip():
            return jsonify({"error": "title cannot be empty"}), 400
        db.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?",
                (title, done, task_id))
    return jsonify({"id": task_id, "title": title, "done": done})

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as db:
        cur = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "task not found"}), 404
    return jsonify({"message": "task deleted"})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)