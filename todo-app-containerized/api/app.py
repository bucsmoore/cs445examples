import json
import os
import uuid

import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

# Get Redis connection details from environment variables
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# Connect to Redis
try:
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    r.ping()  # Test the connection
    print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    # In a real app, you might want to exit or handle this more gracefully


# --- Health Check Endpoint ---
@app.route("/", methods=["GET"])
def health_check():
    """Simple endpoint for health checks."""
    return jsonify({"status": "API is healthy"}), 200


# --- API Endpoints ---


@app.route("/createtask", methods=["POST"])
def create_task():
    description = request.form.get("description")
    if not description:
        return jsonify({"error": "Description is required"}), 400

    task_id = str(uuid.uuid4())  # Generate a unique ID for the task
    task = {"id": task_id, "description": description, "completed": False}

    # Store task as a JSON string in Redis
    r.set(f"task:{task_id}", json.dumps(task))
    return jsonify(task), 201


@app.route("/loadtasks", methods=["GET"])
def load_tasks():
    tasks = []
    # Get all keys that start with "task:"
    task_keys = r.keys("task:*")
    for key in task_keys:
        task_data = r.get(key)
        if task_data:
            tasks.append(json.loads(task_data))

    # Sort tasks by creation/ID for consistent order (optional)
    tasks.sort(key=lambda t: t["id"])

    return jsonify(tasks), 200


@app.route("/edittask/<string:task_id>", methods=["PUT"])
def edit_task(task_id):
    task_key = f"task:{task_id}"
    existing_task_data = r.get(task_key)

    if not existing_task_data:
        return jsonify({"error": "Task not found"}), 404

    existing_task = json.loads(existing_task_data)

    # HTMX sends form data, so check request.form
    if "description" in request.form:
        existing_task["description"] = request.form.get("description")
    if "completed" in request.form:
        # request.form.get('completed') will be 'true' or 'false' string from JS checkbox
        existing_task["completed"] = request.form.get("completed").lower() == "true"

    r.set(task_key, json.dumps(existing_task))
    return jsonify(existing_task), 200


@app.route("/deletetask/<string:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_key = f"task:{task_id}"
    deleted_count = r.delete(task_key)

    if deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": f"Task {task_id} deleted"}), 200


if __name__ == "__main__":
    # Run the Flask app on all available interfaces
    app.run(host="0.0.0.0")
