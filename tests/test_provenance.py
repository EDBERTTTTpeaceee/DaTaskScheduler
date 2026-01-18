import unittest
from src.provenance import task_signature, profile_repository

class ProvenanceTests(unittest.TestCase):

    def test_task_signature_basic(self):
        t = {"id": "x1", "title": "Study AI 📚"}
        s = task_signature(t)
        self.assertIn("signature", s)
        self.assertEqual(s["id"], "x1")
        self.assertGreaterEqual(s["trigram_count"], 1)
        self.assertIsInstance(s["uniqueness_score"], float)

    def test_profile_repository_empty(self):
        p = profile_repository([], metadata=None)
        self.assertEqual(p["n_tasks"], 0)
        self.assertEqual(p["top_signatures"], [])

if __name__ == "__main__":
    unittest.main()
