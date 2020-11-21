import sys
import csv
import json
from flask import Flask, render_template, request, jsonify, make_response
from data.students import sample_data_students
from data.courses import sample_data_courses
from data.cities import sample_data_cities

""" replace with either "MySQL", "SQLite" or "SQLAlchemy" to switch database module """
DATABASE_MODULE = "MySQL"

arg = DATABASE_MODULE.lower()
if arg == "mysql":
    import mymodules.mysql_module as db
elif arg == "sqlaLchemy":
    import mymodules.sqlalchemy_module as db
elif arg == "sqlite":
    import mymodules.sqlite_module as db
else:
    sys.exit("Invalid database module in DATABASE_MODULE variable")

app = Flask(__name__)


def reset():
    try:
        db.drop_everything()
    except Exception as e:
        print("Table does not exist: ", e)


""" ROUTES """


@app.route('/')
def index():
    """
    Note: The styling parameter takes any value for now and,
        if present in the querystring,
        renders the template without bootstrap.css, JQuery and bootstrap.js,
        using style.css instead.
    :return:
    """
    context = {
        "student_list": db.get_all_students(),
        "table_list": db.get_all_tables(),
        "theme": request.args.get('theme')
    }
    return render_template('base.html', **context)


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route('/insert/sample-data', methods=["POST"])
def insert_sample_data():
    """
    Returns status code 500 server error if failing to insert
    :return:
    """
    try:
        """ Preparing cities
            These have to be inserted first, 
            due to foreign key constrains in the student table
        """
        cities_for_sql_insert = []
        for city in sample_data_cities:
            tuple_object = (city["city_id"], city["name"], city["country"])
            cities_for_sql_insert.append(tuple_object)

        """ Preparing students 
            As we have a NOT NULL Constraint on given_name and family_name
            we need to compensate for this in our application logic since
            the student data has missing values, 
            or in some way not adhering to our database design
        """
        students_for_sql_insert = []
        for student in sample_data_students:
            if student["family_name"] is None:
                student["family_name"] = "Unknown"
            tuple_object = (student["given_name"], student["family_name"], student.get("location_city"))
            students_for_sql_insert.append(tuple_object)

        """ Preparing courses
        """
        courses_for_sql_insert = []
        for c in sample_data_courses:
            tuple_object = (c["course_id"], c["topic"], c["datetime"])
            courses_for_sql_insert.append(tuple_object)

        """ Inserts all sample data in one go """
        db.insert_sample_data(
            cities_for_sql_insert,
            students_for_sql_insert,
            courses_for_sql_insert
        )
        return make_response("Sample data successfully inserted into database")
    except Exception as e:
        response_message = "Something went wrong: " + str(e)
        print(response_message)
        return make_response(response_message, 500)


@app.route('/create/stuff', methods=["POST"])
def create_stuff():
    request_data = request.get_json()
    action = request_data['action']
    result = {
        "ok": False,
        "action": action,
    }
    if action == "make a table for our students":
        db.create_table()
        result["ok"] = True
    elif action == "delete everything":
        reset()
        result["ok"] = True
        result["message"] = "Ready to start over"
    elif action == "delete student":
        student_id = request_data["student_id"]
        result_delete = db.delete_student(student_id)
        result["ok"] = result_delete
        result["message"] = "Deleted student" if result_delete else "Unable to delete student"
    return jsonify(result)


@app.route('/export/<export_type>', methods=["GET"])
def export(export_type):
    result = db.get_all_students()
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
        file = open('students.csv', newline='')
        return "<pre>" + file.read() + "</pre>"
    else:
        return "Try json or csv"
