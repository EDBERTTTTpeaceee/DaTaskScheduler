import unittest
from src.main import remove_task_by_id


class DeleteTaskTests(unittest.TestCase):

    def setUp(self):
        self.tasks = [
            {"id": "a1", "title": "Task A", "due_date": ""},
            {"id": "b2", "title": "Task B", "due_date": ""},
            {"id": "c3", "title": "Task C", "due_date": ""}
        ]

    def test_delete_existing_task(self):
        remaining, found = remove_task_by_id(self.tasks, "b2")

        self.assertTrue(found)
        self.assertEqual(len(remaining), 2)
        self.assertNotIn("b2", [t["id"] for t in remaining])

    def test_delete_nonexistent_task(self):
        remaining, found = remove_task_by_id(self.tasks, "x9")

        self.assertFalse(found)
        self.assertEqual(len(remaining), 3)
