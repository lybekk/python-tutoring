import sqlite3


def connect():
    connection = sqlite3.connect('training.db')
    return connection


def commit_statement(statement, values=None):
    try:
        db = connect()
        with db:
            mycursor = db.cursor()
            if values:
                mycursor.execute(statement, values)
            else:
                mycursor.execute(statement)
    except Exception as e:
        print(e)


def commit_statement_many(statement, list_of_inserts):
    try:
        db = connect()
        with db:
            mycursor = db.cursor()
            mycursor.executemany(statement, list_of_inserts)
    except Exception as e:
        print(e)


def create_table():
    commit_statement("""
    CREATE TABLE IF NOT EXISTS cities (
        "city_id"		INTEGER NOT NULL UNIQUE,
        "name"			TEXT NOT NULL,
        "country"		TEXT NOT NULL,
        PRIMARY KEY("city_id")
    );
    """)
    commit_statement("""
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
    commit_statement("""
    CREATE TABLE IF NOT EXISTS courses (
        "course_id"	INTEGER NOT NULL UNIQUE,
        "topic"			TEXT NOT NULL,
        "datetime"		TEXT NOT NULL,
        PRIMARY KEY("course_id")
    );
    """)


def drop_everything():
    commit_statement("DROP TABLE IF EXISTS students;")
    commit_statement("DROP TABLE IF EXISTS cities;")
    commit_statement("DROP TABLE IF EXISTS courses;")


def insert_sample_data(cities, students, courses):
    sql_executions = [
        ['INSERT INTO cities (city_id,name, country) VALUES (?,?,?)', cities],
        ['INSERT INTO students (given_name, family_name, date_birth, location_city) VALUES (?,?,?,?)', students],
        ['INSERT INTO courses (course_id, topic, datetime) VALUES (?,?,?)', courses]
    ]
    for item in sql_executions:
        commit_statement_many(item[0], item[1])


def get_all_students():
    try:
        data = []
        db = connect()
        with db:
            mycursor = db.cursor()
            mycursor.execute("""
                SELECT students.student_id, students.given_name, students.family_name, IFNULL(cities.name, 'Unknown') AS city 
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


def get_all_tables():
    try:
        db = connect()
        with db:
            mycursor = db.cursor()
            table_names = []
            for name in mycursor.execute('SELECT name FROM sqlite_master'):
                if not name[0].startswith("sqlite"):
                    table_names.append(name[0])
            return table_names
    except Exception as e:
        print(e)
        return []


def delete_student(student_id):
    try:
        db = connect()
        with db:
            commit_statement("DELETE FROM students WHERE student_id=?", (student_id,))
        return True
    except Exception as e:
        print(e)
        return False


def get_data_batch():
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
