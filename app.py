from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage. Resets whenever the app restarts.
tasks = []
next_id = 1


@app.route("/tasks", methods=["POST"])
def add_task():
    """Add a new task. Body: {"title": "buy milk"}"""
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "title is required"}), 400

    global next_id
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks", methods=["GET"])
def list_tasks():
    """List all tasks."""
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>/done", methods=["PATCH"])
def mark_done(task_id):
    """Mark a task as done."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return jsonify(task), 200

    return jsonify({"error": "task not found"}), 404


@app.route("/health", methods=["GET"])
def health():
    """Basic health check, mostly useful for confirming the container is up."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
