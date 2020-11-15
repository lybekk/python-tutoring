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

sqlite_drop_student_table = "DROP TABLE python_students;"
