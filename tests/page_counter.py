import unittest
from routes.domain import PageStatistics


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.page_stat = PageStatistics()

    def test_initialize(self):
        self.assertEqual(self.page_stat.count, 0)
        self.assertEqual(self.page_stat.visitors, set())

    def test_visit(self):
        self.page_stat.visit(12345)
        self.assertEqual(self.page_stat.count, 1)
        self.assertTrue(12345 in self.page_stat.visitors)


if __name__ == "__main__":
    unittest.main()
