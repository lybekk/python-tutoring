import sqlite3

connection = sqlite3.connect('training.db')
mycursor = connection.cursor()

new_cell_value = "N/A"
value_to_replace = "Unknown"

sql_statement = """
UPDATE python_students
SET family_name=?
WHERE family_name=?
"""
mycursor.execute(sql_statement, (new_cell_value, value_to_replace,))
connection.commit()
connection.close()
