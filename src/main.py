import sys
from datetime import datetime
from src.storage import load_tasks, save_tasks
from src.task import create_task


def _parse_date_or_max(s):
    if not s:
        return datetime.max
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.max


def remove_task_by_id(tasks, task_id):
    remaining = []
    found = False

    for t in tasks:
        if t["id"] == task_id:
            found = True
        else:
            remaining.append(t)

    return remaining, found

def find_tasks_by_title(tasks, title):
    title_lower = title.strip().lower()
    matches = []

    for t in tasks:
        if t["title"].lower() == title_lower:
            matches.append(t)

    return matches

def delete_task_by_name(title):
    tasks = load_tasks()
    matches = find_tasks_by_title(tasks, title)

    if not matches:
        print("No task found with that title.")
        return

    if len(matches) > 1:
        print("Multiple tasks have this title. Use delete-id instead.")
        return

    task_id = matches[0]["id"]
    remaining, _ = remove_task_by_id(tasks, task_id)

    save_tasks(remaining)
    print("Task deleted.")


def add_task():
    tasks = load_tasks()

    while True:
        title = input("Enter task title: ")
        due = input("Enter due date (YYYY-MM-DD) — leave blank if none: ")

        try:
            task = create_task(title, due)
            break
        except ValueError as e:
            print(e)
            print("Please try again.\n")

    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")

def list_tasks():
    tasks = load_tasks()

    tasks_sorted = sorted(
        tasks,
        key=lambda t: _parse_date_or_max(t.get("due_date", ""))
    )

    print("\nTasks:")
    for t in tasks_sorted:
        due_display = t.get("due_date") or "no date"
        print(f"- {t['id']}: {t['title']} (due: {due_display})")


def delete_task(task_id):
    tasks = load_tasks()

    remaining, found = remove_task_by_id(tasks, task_id)

    if not found:
        print("No task found with that ID.")
        return

    save_tasks(remaining)
    print("Task deleted.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py [add | list | delete <id>]")
        return

    command = sys.argv[1]

    if command == "add":
        add_task()
    elif command == "list":
        list_tasks()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python src/main.py delete <task_id>")
            return
        delete_task(sys.argv[2])
    else:
        print("Unknown command:", command)
        print("Usage: python src/main.py [add | list | delete <id>] | delete-name <title>")


if __name__ == "__main__":
    main()
