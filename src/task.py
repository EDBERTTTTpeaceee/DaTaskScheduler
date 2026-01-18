import uuid
from datetime import datetime


def parse_due_date(due):
    if not due:
        return ""

    try:
        parsed = datetime.strptime(due, "%Y-%m-%d")
        return parsed.date().isoformat()
    except ValueError:
        raise ValueError("Due date must be a real date in YYYY-MM-DD format.")


def create_task(title, due):
    cleaned_title = title.strip()

    if not cleaned_title:
        raise ValueError("Task title cannot be empty.")

    return {
        "id": str(uuid.uuid4()),
        "title": cleaned_title,
        "due_date": parse_due_date(due)
    }


