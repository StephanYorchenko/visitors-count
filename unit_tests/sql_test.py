import os
import sqlite3
import unittest
from datetime import datetime
from os.path import isfile

from infrastucture import SQLExecutor


class SQLExecutorTests(unittest.TestCase):
    def setUp(self):
        self.name = "test_base.db"
        try:
            os.remove(self.name)
        except FileNotFoundError:
            pass
        self.sql_executor = SQLExecutor(self.name)

    def test_initialize(self):
        self.assertTrue(isfile(self.name))
        with sqlite3.connect(self.name) as con:
            cursor = con.cursor()
            cursor.execute("PRAGMA table_info(visits);")
            a = list(map(lambda x: (x[1], x[2]), cursor.fetchall()))
        self.assertListEqual(
            a,
            [("page_id", "INTEGER"),
             ("client_id", "TEXT"),
             ("visit_time", "TEXT")]
        )

    def test_execute(self):
        sqls = [
            "SELECT * FROM visits;",
            "SELECT page_id FROM visits;",
            "SELECT * FROM visits WHERE page_id=1",
            "SELECT 1 FROM visits WHERE page_id=1",
        ]
        with sqlite3.connect(self.name) as con:
            cursor = con.cursor()
            for i in range(10):
                cursor.execute(
                    f"INSERT INTO visits "
                    f"(page_id, client_id, visit_time) "
                    f"VALUES ({i}, {i * 13},"
                    f" '2020-12-27 12:43:00')"
                )
                cursor.fetchall()
            expected = []
            for sql in sqls:
                cursor.execute(sql)
                expected.append(cursor.fetchall())
        actual = [self.sql_executor.execute(sql) for sql in sqls]
        self.assertListEqual(expected, actual)

    def test_insert(self):
        self.sql_executor.try_insert(
            "visits",
            page_id=13,
            client_id='"wropfdjkklahfu14rqry-c08r-"',
            visit_time='"2020-12-27 12:43:00"',
        )
        with sqlite3.connect(self.name) as con:
            cursor = con.cursor()
            cursor.execute("SELECT page_id FROM visits WHERE page_id=13;")
            res = cursor.fetchall()

        self.assertEqual(res, [(13,)])

    def test_select_by_dates(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_time = "2000-12-27 " + datetime.now().strftime("%H:%M:%S")
        records = [
            (156, "qwertyuio", last_time),
            (156, "asdfghjkl", last_time),
            (156, "qqwervbnm", last_time),
            (156, "qwertyuio", last_time),
            (156, "qwertyuio", now),
            (156, "qwertyuio", now),
        ]
        with sqlite3.connect(self.name) as con:
            cursor = con.cursor()
            cursor.executemany(
                "INSERT INTO visits (page_id, client_id, visit_time) "
                "VALUES (?, ?, ?)",
                records,
            )
            cursor.fetchall()

        self.assertEqual(
            len(self.sql_executor.select_for_days("-4000 year", 156)), 6)
        self.assertEqual(
            len(self.sql_executor.select_for_days("-1 day", 156)), 2)

    def test_count_all(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_time = "2000-12-27 " + datetime.now().strftime("%H:%M:%S")
        records = [
            (156, "qwertyuio", last_time),
            (156, "asdfghjkl", last_time),
            (156, "qqwervbnm", last_time),
            (156, "qwertyuio", last_time),
            (156, "qwert457o", now),
            (156, "qwertyuio", now),
            (156, "qwertyuio", now),
        ]
        with sqlite3.connect(self.name) as con:
            cursor = con.cursor()
            cursor.executemany(
                "INSERT INTO visits (page_id, client_id, visit_time) "
                "VALUES (?, ?, ?)",
                records,
            )
            cursor.fetchall()

        self.assertEqual(
             self.sql_executor.count_all(156, "-1 day", unique=True), 2)
        self.assertEqual(
             self.sql_executor.count_all(156, "-4000 year", unique=True), 4)
        self.assertEqual(self.sql_executor.count_all(156, "-1 day"), 3)
        self.assertEqual(
             self.sql_executor.count_all(156, "-4000 year"), len(records))


if __name__ == "__main__":
    unittest.main()
