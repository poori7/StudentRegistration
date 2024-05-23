import logging
from flask import Flask, request, redirect, flash, render_template
import datetime
import decimal
import config
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'Darshitha#123'

# CORS to avoid 'Access-Control-Allow-Origin' error
CORS(app)

# Create MySQL connection
db = mysql.connector.connect(host=config._DB_CONF['host'],
                             port=config._DB_CONF['port'],
                             user=config._DB_CONF['user'],
                             passwd=config._DB_CONF['passwd'],
                             db=config._DB_CONF['db'])

# Serialization function for types
def type_handler(x):
    """Type serialization function."""
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    if isinstance(x, decimal.Decimal):
        return '$%.2f' % x
    raise TypeError("Unknown type")

@app.route('/')
def index():
    """Web service test method."""
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM registrations")
        reg = cursor.fetchall()

    return render_template('index.html', reg=reg)

@app.route('/form')
def form():
    return render_template('form.html')

# Define the route for handling the form submission
@app.route('/add', methods=['POST'])
def insert():
    # Get the form data
    id = int(request.form['id'])
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']
    email = request.form['email']

    with db.cursor() as cursor:
        query = "INSERT INTO registrations (id, name, age, address, email) VALUES (%s, %s, %s, %s, %s)"
        values = (id, name, age, address, email)
        cursor.execute(query, values)
        db.commit()

    # Set a flash message to notify the user that the row has been added
    flash("Data added successfully.", "success")

    # Redirect the user back to the student data page
    return redirect('/')

@app.route('/update', methods=['POST'])
def update():
    # Get the form data
    id = int(request.form['id'])  # Convert id to integer
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']
    email = request.form['email']

    with db.cursor() as cursor:
        cursor.execute('UPDATE registrations SET name=%s, age=%s, address=%s, email=%s WHERE id=%s', (name, age, address, email, id))
        db.commit()

    # Redirect the user back to the student data page
    return redirect('/')

# Define the route to handle the deletion of a student
@app.route('/delete/<int:id>')
def delete_student(id):
    with db.cursor() as cursor:
        # Execute the DELETE query to remove the student from the database
        cursor.execute("DELETE FROM registrations WHERE id=%s", (id,))
        # Commit the changes to the database
        db.commit()

    # Redirect the user back to the student data page
    return redirect('/')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099, debug=True)