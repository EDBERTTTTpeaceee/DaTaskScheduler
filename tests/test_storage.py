import unittest
import os
import json
from src.storage import save_tasks, load_tasks, DATA_FILE

TEST_BACKUP = "data/tasks.json.bak_for_tests"

class StorageTests(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DATA_FILE):
            os.rename(DATA_FILE, TEST_BACKUP)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        if os.path.exists(TEST_BACKUP):
            os.rename(TEST_BACKUP, DATA_FILE)

    def test_save_and_load_roundtrip(self):
        tasks = [{"id": "a", "title": "t1", "due_date": ""}]
        save_tasks(tasks)
        loaded = load_tasks()
        self.assertIsInstance(loaded, list)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "a")
        self.assertEqual(loaded[0]["title"], "t1")

if __name__ == "__main__":
    unittest.main()
