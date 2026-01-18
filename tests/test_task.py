import unittest
from src.task import create_task

class TaskModelTests(unittest.TestCase):
    def test_create_task_has_id_title_and_due(self):
        t = create_task("example", "2026-01-30")
        self.assertIn("id", t)
        self.assertIn("title", t)
        self.assertIn("due_date", t)
        self.assertEqual(t["title"], "example")
        self.assertEqual(t["due_date"], "2026-01-30")
    
    def test_empty_title_raises_error(self):
        with self.assertRaises(ValueError):
            create_task("   ", "")

    def test_invalid_date_raises_error(self):
        with self.assertRaises(ValueError):
            create_task("Test", "2025-99-99")

    def test_valid_date_is_saved(self):
        task = create_task("Test", "2025-12-31")
        self.assertEqual(task["due_date"], "2025-12-31")


if __name__ == "__main__":
    unittest.main()
