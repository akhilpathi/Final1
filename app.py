from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database configuration
DATABASE = 'database.db'

def create_tables():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS department (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email_id TEXT NOT NULL,
                phoneNumber TEXT NOT NULL,
                deptId INTEGER NOT NULL,
                FOREIGN KEY (deptId) REFERENCES department (id)
            )
        ''')
        connection.commit()

# Create tables on startup
create_tables()

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        # Fetch all students with department names
        cursor.execute('''
            SELECT student.id, student.name, student.email_id, student.phoneNumber, department.name
            FROM student
            JOIN department ON student.deptId = department.id
        ''')
        students = cursor.fetchall()

        # Fetch all departments
        cursor.execute('SELECT * FROM department')
        departments = cursor.fetchall()

    return render_template('index.html', students=students, departments=departments)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    email_id = request.form['email_id']
    phoneNumber = request.form['phoneNumber']
    deptId = request.form['deptId']

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO student (name, email_id, phoneNumber, deptId) VALUES (?, ?, ?, ?)', (name, email_id, phoneNumber, deptId))
        connection.commit()

    return redirect(url_for('index'))

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'GET':
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            # Fetch student details
            cursor.execute('SELECT * FROM student WHERE id = ?', (student_id,))
            student = cursor.fetchone()

            # Fetch all departments
            cursor.execute('SELECT * FROM department')
            departments = cursor.fetchall()

        return render_template('edit_student.html', student=student, departments=departments)
    elif request.method == 'POST':
        name = request.form['name']
        email_id = request.form['email_id']
        phoneNumber = request.form['phoneNumber']
        deptId = request.form['deptId']

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE student
                SET name=?, email_id=?, phoneNumber=?, deptId=?
                WHERE id=?
            ''', (name, email_id, phoneNumber, deptId, student_id))
            connection.commit()

        return redirect(url_for('index'))

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM student WHERE id = ?', (student_id,))
        connection.commit()

    return redirect(url_for('index'))

@app.route('/add_department', methods=['POST'])
def add_department():
    name = request.form['name']

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO department (name) VALUES (?)', (name,))
        connection.commit()

    return redirect(url_for('index'))

@app.route('/edit_department/<int:dept_id>', methods=['GET', 'POST'])
def edit_department(dept_id):
    if request.method == 'GET':
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            # Fetch department details
            cursor.execute('SELECT * FROM department WHERE id = ?', (dept_id,))
            department = cursor.fetchone()

        return render_template('edit_department.html', department=department)
    elif request.method == 'POST':
        name = request.form['name']

        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE department SET name=? WHERE id=?', (name, dept_id))
            connection.commit()

        return redirect(url_for('index'))

@app.route('/delete_department/<int:dept_id>')
def delete_department(dept_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM department WHERE id = ?', (dept_id,))
        connection.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
