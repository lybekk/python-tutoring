from unittest import TestCase
import sqlite3
from mymodules.sqlite_module import DatabaseSQLite


class TestDatabaseSQLite(TestCase):
    def setUp(self):
        self.db = DatabaseSQLite("testing.db")

    def test_connect(self):
        connection = self.db.connect()
        self.assertEqual(isinstance(connection, sqlite3.Connection), True)

    def test_connection_test(self):
        print("Database path", self.db.db_path)
        check = self.db.db_path.is_file()
        print(check)
        self.assertEqual(check, True)

    def test_create_table(self):
        self.fail()

    def test_drop_everything(self):
        self.fail()
