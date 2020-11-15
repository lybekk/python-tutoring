sqlite_create_student_table = """
CREATE TABLE IF NOT EXISTS python_students (
    "student_id"	INTEGER NOT NULL UNIQUE,
    "given_name"	TEXT NOT NULL DEFAULT 'Unknown',
    "family_name"	TEXT NOT NULL DEFAULT 'Unknown',
    "location_city"	TEXT,
    "longitude"	REAL,
    "latitude"	REAL,
    PRIMARY KEY("student_id" AUTOINCREMENT)
);
"""

sqlite_create_courses_table = """
CREATE TABLE IF NOT EXISTS courses (
    "courses_id"	INTEGER NOT NULL UNIQUE,
    "topic"			TEXT NOT NULL,
    "datetime"		TEXT NOT NULL
    PRIMARY KEY("courses_id")
);
"""

sqlite_create_cities_table = """
CREATE TABLE IF NOT EXISTS cities (
    "city_id"		TEXT NOT NULL UNIQUE,
    "name"			TEXT NOT NULL,
    "country"		TEXT NOT NULL,
    PRIMARY KEY("city_id")
);
"""

sqlite_drop_student_table = "DROP TABLE python_students;"
