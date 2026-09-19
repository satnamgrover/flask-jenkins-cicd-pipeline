from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" of tasks - simple enough to keep the demo focused
# on the pipeline, not the app.
tasks = {}
next_id = 1


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint - used by load balancers / uptime checks."""
    return jsonify({"status": "healthy"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(list(tasks.values())), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json(silent=True)

    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "done": False,
    }
    tasks[next_id] = task
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    task = tasks.get(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404
    task["done"] = True
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404
    del tasks[task_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
