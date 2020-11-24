import mysql.connector
from mymodules.settings import settings


def connect_fallback():
    # TODO: this
    """WORK IN PROGRESS"""
    connection = mysql.connector.connect(
        host=settings["host"],
        user=settings["user"],
        password=settings["password"],
    )
    mycursor = connection.cursor()
    mycursor.execute("CREATE DATABASE mydatabase")
    connection.commit()


def connect():
    try:
        connection = mysql.connector.connect(
            host=settings["host"],
            user=settings["user"],
            password=settings["password"],
            database="mydatabase"
        )
        return connection
    except Exception as e:
        print(e)


def commit_statement(statement, values=None):
    try:
        db = connect()
        with db:
            mycursor = db.cursor()
            if values:
                mycursor.execute(statement, values)
            else:
                mycursor.execute(statement)
            db.commit()
    except Exception as e:
        print(e)


def commit_statement_many(statement, list_of_inserts):
    try:
        db = connect()
        with db:
            mycursor = db.cursor()
            mycursor.executemany(statement, list_of_inserts)
            db.commit()
    except Exception as e:
        print(e)


def create_table():
    commit_statement("""
    CREATE TABLE IF NOT EXISTS `mydatabase`.`cities` (
        `city_id` INT NOT NULL,
        `name` VARCHAR(45) NOT NULL,
        `country` VARCHAR(45) NOT NULL,
        PRIMARY KEY (`city_id`),
        UNIQUE INDEX `city_id_UNIQUE` (`city_id` ASC) VISIBLE
    );
    """)
    commit_statement("""CREATE TABLE IF NOT EXISTS `mydatabase`.`students` (
        `student_id` INT NOT NULL AUTO_INCREMENT,
        `given_name` VARCHAR(90) NOT NULL DEFAULT 'Unknown',
        `family_name` VARCHAR(90) NOT NULL DEFAULT 'Unknown',
        `date_birth` DATETIME NULL,
        `location_city` INT NULL,
        `coordinates` POINT NULL,
        PRIMARY KEY (`student_id`),
        UNIQUE INDEX `student_id_UNIQUE` (`student_id` ASC) VISIBLE,
        INDEX `city_id_idx` (`location_city` ASC) VISIBLE,
        CONSTRAINT `city_id`
            FOREIGN KEY (`location_city`)
            REFERENCES `mydatabase`.`cities` (`city_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
    """)
    commit_statement("""CREATE TABLE `mydatabase`.`courses` (
        `course_id` INT NOT NULL,
        `topic` VARCHAR(180) NOT NULL,
        `datetime` DATETIME NOT NULL,
        PRIMARY KEY (`course_id`),
        UNIQUE INDEX `course_id_UNIQUE` (`course_id` ASC) VISIBLE
    );
    """)


def get_all_students():
    """
    We are using a LEFT JOIN here, since we want all rows from "students",
        and only connect/reference a city from the "cities" table.
    A RIGHT JOIN woul return all cities, with referenced student cells,
        filtering out students with no match in the "cities" table.
    An INNER JOIN would have only given us the rows where students AND cities found a match in both tables.
    A FULL OUTER JOIN does not work on this query.
    :return:
    """
    try:
        db = connect()
        with db:
            mycursor = db.cursor(dictionary=True)
            mycursor.execute("""
                SELECT  students.student_id, 
                        students.given_name, 
                        students.family_name, 
                        IFNULL(cities.name, 'Unknown') AS city 
                FROM students 
                LEFT JOIN cities ON students.location_city=cities.city_id
                ORDER BY students.given_name;
            """)
            data = mycursor.fetchall()
            print(data)
            return data
    except Exception as e:
        print("Error when fetchin students: ", e)
        return []


def get_all_tables():
    try:
        db = connect()
        with db:
            mycursor = db.cursor()
            table_names = []
            mycursor.execute('SHOW TABLES;')
            for name in mycursor:
                table_names.append(name[0])
            return table_names
    except Exception as e:
        print(e)
        return []


def drop_everything():
    commit_statement("""
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS cities;
        DROP TABLE IF EXISTS courses;
    """)


def insert_sample_data(cities, students, courses):
    sql_executions = [
        ['INSERT INTO cities (city_id, name, country) VALUES (%s, %s, %s)', cities],
        ['INSERT INTO students (given_name, family_name, date_birth,location_city) VALUES (%s, %s, %s, %s)', students],
        ['INSERT INTO courses (course_id, topic, datetime) VALUES (%s, %s, %s)', courses]
    ]
    for item in sql_executions:
        commit_statement_many(item[0], item[1])


def delete_student(student_id):
    try:
        db = connect()
        with db:
            commit_statement("DELETE FROM students WHERE student_id=%s", (student_id,))
        return True
    except Exception as e:
        print(e)
        return False


def simple_select(query):
    try:
        db = connect()
        with db:
            mycursor = db.cursor(dictionary=True)
            mycursor.execute(query)
            data = mycursor.fetchall()
            return data
    except Exception as e:
        print("Error when running query: ", query, e)
        return []


def get_data_batch():
    data_batch = {
        "students_born_before_todays_date": simple_select(
            """ SELECT given_name, DATE_FORMAT(date_birth, "%W %M %e %Y") AS date_birth 
                FROM students 
                WHERE date_birth <= CURDATE();
        """),
        "students_born_after_todays_date": simple_select(
            """ SELECT given_name, DATE_FORMAT(date_birth, "%W %M %e %Y") AS date_birth
                FROM students 
                WHERE date_birth >= CURDATE();
        """),
        "count_cities": simple_select(
            """ SELECT  IFNULL(cities.name, 'Unknown') AS city,
                        COUNT(*) as count
                FROM students 
                LEFT JOIN cities ON students.location_city=cities.city_id
                GROUP BY city
                ORDER BY count DESC;
        """),
    }
    print(data_batch)
    return data_batch
