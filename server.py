from flask import Flask, render_template, request, jsonify, make_response
import csv
import json
import sqlite3
import data.statements as sql_statement
import data.students as sample_data_students
import data.courses as sample_data_courses
import data.cities as sample_data_cities

app = Flask(__name__)


def create_table():
    connection = sqlite3.connect('training.db')
    mycursor = connection.cursor()
    mycursor.execute(sql_statement.sqlite_create_student_table)
    mycursor.execute(sql_statement.sqlite_create_courses_table)
    mycursor.execute(sql_statement.sqlite_create_cities_table)
    connection.commit()
    connection.close()


def reset():
    try:
        connection = sqlite3.connect('training.db')
        mycursor = connection.cursor()
        mycursor.execute(sql_statement.sqlite_drop_student_table)
        connection.commit()
        connection.close()
    except Exception as e:
        print("Table does not exist: ", e)


def insert_students():
    try:
        list_of_students_for_sql_insert = []
        for student in sample_data_students.list_students:
            """
            As we have a NOT NULL Constraint on given_name and family_name
            we need to compensate for this in our application logic since
            the student data has missing values, 
            or in some way not adhering to our database design
            """
            if student["family_name"] is None:
                student["family_name"] = "Unknown"
            tuple_object = (student["given_name"], student["family_name"])
            list_of_students_for_sql_insert.append(tuple_object)
        print(list_of_students_for_sql_insert)
        connection = sqlite3.connect('training.db')
        mycursor = connection.cursor()
        mycursor.executemany('INSERT INTO python_students (given_name,family_name) VALUES (?,?)', list_of_students_for_sql_insert)
        connection.commit()
        connection.close()
        return {
            "ok": True,
            "message": "Students successfully inserted into database"
        }
    except Exception as e:
        text = "Something went wrong: " + str(e)
        print(text)
        return {
            "ok": False,
            "message": text
        }


def get_all_students():
    result = []
    try:
        connection = sqlite3.connect('training.db')
        mycursor = connection.cursor()
        query_result = mycursor.execute(
            """SELECT student_id, given_name, family_name FROM python_students ORDER BY given_name"""
        )
        for row in query_result.fetchall():
            dictionary_object = {
                "student_id": row[0],
                "given_name": row[1],
                "family_name": row[2],
            }
            result.append(dictionary_object)
        connection.close()
    except Exception as e:
        print("Student table does not exist: ", e)
    return result


def delete_student(student_id):
    print("Deleting student: ", student_id)
    try:
        connection = sqlite3.connect('training.db')
        mycursor = connection.cursor()
        sql_string = "DELETE FROM python_students WHERE student_id=?"
        # TODO: Test what happens if student id is None or missing
        mycursor.execute(sql_string, (student_id,))
        connection.commit()
        return {
            "ok": True,
            "message": f"Delete student {student_id} success"
        }
    except Exception as e:
        print("Error deleting student: ", e)
        return {
            "ok": False,
            "message": "Error deleting student: " + str(e)
        }


""" ROUTES """


@app.route('/')
def index():
    return render_template('base.html', student_list=get_all_students())


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route('/create/stuff', methods=["POST"])
def create_stuff():
    request_data = request.get_json()
    action = request_data['action']
    result = {
        "ok": False,
        "action": action,
    }
    if action == "make a table for our students":
        create_table()
        result["ok"] = True
    elif action == "insert sample data":
        insert_response = insert_students()
        insert_response2 = insert_cities()
        #insert_response3 = insert_courses()
        result["ok"] = insert_response["ok"]
        if not insert_response["ok"]:
            result["ok"] = False
        result["message"] = insert_response["message"]
    elif action == "delete everything":
        reset()
        result["ok"] = True
        result["message"] = "Ready to start over"
    elif action == "delete student":
        student_id = request_data["student_id"]
        result_delete = delete_student(student_id)
        result["ok"] = result_delete["ok"]
        result["message"] = result_delete["message"]
    return jsonify(result)


@app.route('/export/<export_type>', methods=["GET"])
def export(export_type):
    result = get_all_students()
    if export_type == "json":
        with open('students.json', "w") as file:
            dump = json.dumps(result, indent=4)
            file.write(dump)
        return jsonify(result)
    elif export_type == "csv":
        with open('students.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["First name", "Last name"])
            for student in result:
                spamwriter.writerow([student["given_name"], student["family_name"]])
        file = open('students.csv', 'r', newline='')
        return "<pre>" + file.read() + "</pre>"
    else:
        return "Try json or csv"
