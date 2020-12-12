import pathlib
import sqlite3
from mymodules.config import Config


class DatabaseSQLite:
    """SQLite
    """
    def __init__(self, file_name):
        self.config = Config()
        self.db_name = file_name
        self.db_path = pathlib.Path(__file__).parent.absolute().parent.absolute().joinpath(self.db_name)

    def connection_test(self):
        """Tests the connection to the database file (usually training.db).
        In this case, it checks if the .db file is available,
        or if it doesn't exist, it will try to create it.

        Returns:
            dict: Returns a dictionary with a boolean retry key. If True, triggers a redirect in Flask
        """
        return {
            "retry": not self.db_path.is_file(),
            "message": ""
        }

    def connect(self):
        """
        Connects to the database file (usually training.db),

        :return:
        """
        connection = sqlite3.connect(self.db_name)
        return connection

    def commit_statement(self, statement, values=None):
        try:
            db = self.connect()
            with db:
                cursor = db.cursor()
                if values:
                    cursor.execute(statement, values)
                else:
                    cursor.execute(statement)
        except Exception as e:
            print(e)

    def commit_statement_many(self, statement, list_of_inserts):
        try:
            db = self.connect()
            with db:
                cursor = db.cursor()
                cursor.executemany(statement, list_of_inserts)
        except Exception as e:
            print(e)

    def create_table(self):
        self.commit_statement("""
        CREATE TABLE IF NOT EXISTS cities (
            "city_id"		INTEGER NOT NULL UNIQUE,
            "name"			TEXT NOT NULL,
            "country"		TEXT NOT NULL,
            PRIMARY KEY("city_id")
        );
        """)
        self.commit_statement("""
        CREATE TABLE IF NOT EXISTS students (
            "student_id"	INTEGER NOT NULL UNIQUE,
            "given_name"	TEXT NOT NULL DEFAULT 'Unknown',
            "family_name"	TEXT NOT NULL DEFAULT 'Unknown',
            "date_birth"	TEXT,
            "location_city"	TEXT,
            "longitude"	REAL,
            "latitude"	REAL,
            PRIMARY KEY("student_id" AUTOINCREMENT)
        );
        """)
        self.commit_statement("""
        CREATE TABLE IF NOT EXISTS courses (
            "course_id"	INTEGER NOT NULL UNIQUE,
            "topic"			TEXT NOT NULL,
            "datetime"		TEXT NOT NULL,
            PRIMARY KEY("course_id")
        );
        """)

    def drop_everything(self):
        self.commit_statement("DROP TABLE IF EXISTS students;")
        self.commit_statement("DROP TABLE IF EXISTS cities;")
        self.commit_statement("DROP TABLE IF EXISTS courses;")

    def insert_sample_data(self, cities, students, courses):
        sql_executions = [
            ['INSERT INTO cities (city_id,name, country) VALUES (?,?,?)', cities],
            ['INSERT INTO students (given_name, family_name, date_birth, location_city) VALUES (?,?,?,?)', students],
            ['INSERT INTO courses (course_id, topic, datetime) VALUES (?,?,?)', courses]
        ]
        for item in sql_executions:
            self.commit_statement_many(item[0], item[1])

    def get_all_students(self):
        try:
            data = []
            db = self.connect()
            with db:
                mycursor = db.cursor()
                mycursor.execute("""
                    SELECT students.student_id, 
                        students.given_name, 
                        students.family_name, 
                        IFNULL(cities.name, 'Unknown') AS city 
                    FROM students 
                    LEFT JOIN cities ON students.location_city=cities.city_id
                    ORDER BY students.given_name;
                """)
                column_names = []
                for column_name in mycursor.description:
                    column_names.append(
                        column_name[0]
                    )
                for row in mycursor.fetchall():
                    data.append(
                        dict(
                            zip(
                                column_names,
                                row
                            )
                        )
                    )
                print(data)
                return data
        except Exception as e:
            print(e)
            return []

    def get_all_tables(self):
        try:
            db = self.connect()
            with db:
                cursor = db.cursor()
                table_names = []
                for name in cursor.execute('SELECT name FROM sqlite_master'):
                    if not name[0].startswith("sqlite"):
                        table_names.append(name[0])
                return table_names
        except Exception as e:
            print(e)
            return []

    def delete_student(self, student_id):
        try:
            db = self.connect()
            with db:
                self.commit_statement("DELETE FROM students WHERE student_id=?", (student_id,))
            return True
        except Exception as e:
            print(e)
            return False

    def get_data_batch(self):
        data_batch = {
            "students_born_before_todays_date": [
                {
                    "given_name": "Not implemented for the SQLite module yet. Use MySQL.",
                    "date_birth": ""
                }
            ],
            "students_born_after_todays_date": [
                {
                    "given_name": "Not implemented for the SQLite module yet. Use MySQL.",
                    "date_birth": ""
                }
            ],
            "count_cities": [
                {
                    "city": "Not implemented for the SQLite module yet. Use MySQL for this feature.",
                    "count": ""
                }
            ],
        }
        return data_batch
