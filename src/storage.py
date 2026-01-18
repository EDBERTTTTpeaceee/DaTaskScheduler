import json
import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "tasks.json")

def ensure_task_id(task):
    if not isinstance(task, dict):
        return None
    if "id" not in task:
        task["id"] = str(uuid.uuid4())
    return task

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

    if not isinstance(tasks, list):
        return []

    for t in tasks:
        ensure_task_id(t)

    return tasks

def save_tasks(tasks):
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)
