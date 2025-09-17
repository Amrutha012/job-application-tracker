import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Initialize database (create table if it doesn't exist)
def init_db():
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student TEXT NOT NULL,
                    company TEXT NOT NULL,
                    position TEXT NOT NULL,
                    status TEXT,
                    applied_on TEXT)''')
    conn.commit()
    conn.close()

# Get DB connection
def get_db_connection():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM applications').fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

# Add new application
@app.route('/add', methods=['POST'])
def add():
    student = request.form['student']
    company = request.form['company']
    position = request.form['position']
    status = request.form['status']
    applied_on = request.form['applied_on']
    conn = get_db_connection()
    conn.execute('INSERT INTO applications (student, company, position, status, applied_on) VALUES (?, ?, ?, ?, ?)',
                 (student, company, position, status, applied_on))
    conn.commit()
    conn.close()
    return redirect('/')

# Update application
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    student = request.form['student']
    company = request.form['company']
    position = request.form['position']
    status = request.form['status']
    applied_on = request.form['applied_on']
    conn = get_db_connection()
    conn.execute('UPDATE applications SET student=?, company=?, position=?, status=?, applied_on=? WHERE id=?',
                 (student, company, position, status, applied_on, id))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete application
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM applications WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()  # Ensure table exists
    app.run(debug=True)
