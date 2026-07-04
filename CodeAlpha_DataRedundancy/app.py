# ==========================================
# Data Redundancy Removal System
# Flask + SQLite Project
# ==========================================

# Import Required Libraries
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Database Initialization
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Records Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL
    )
    """)

    # Duplicate Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS duplicate_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duplicate_type TEXT NOT NULL,
        duplicate_value TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ==========================================
# Add Record Module
# Handles record insertion and duplicate checks
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def add_record():
    message = ""
    alert_type = ""

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Check duplicate email
        cursor.execute(
            "SELECT * FROM records WHERE email=?",
            (email,)
        )

        email_exists = cursor.fetchone()

        # Check duplicate phone
        cursor.execute(
            "SELECT * FROM records WHERE phone=?",
            (phone,)
        )

        phone_exists = cursor.fetchone()

        if email_exists:

            cursor.execute("""
                INSERT INTO duplicate_logs
                (duplicate_type, duplicate_value)
                VALUES (?,?)
            """, (
                "Email",
                email
            ))

            conn.commit()

            message = "Duplicate Email Found"
            alert_type = "danger"

        elif phone_exists:

            cursor.execute("""
                INSERT INTO duplicate_logs
                (duplicate_type, duplicate_value)
                VALUES (?,?)
            """, (
                "Phone",
                phone
            ))

            conn.commit()

            message = "Duplicate Mobile Number Found"
            alert_type = "danger"
        else:
            cursor.execute(
                "INSERT INTO records(name,email,phone) VALUES(?,?,?)",
                (name, email, phone)
            )

            conn.commit()

            message = "Record Added Successfully"
            alert_type = "success"

        conn.close()

    return render_template(
        'add_record.html',
        message=message,
        alert_type=alert_type
    )


# ==========================================
# Records Management Module
# View and search stored records
# ==========================================
@app.route('/records')
def records():
    search = request.args.get('search', '')

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT * FROM records
            WHERE name = ?
            OR email = ?
            OR phone = ?
        """, (search, search, search))
    else:
        cursor.execute("SELECT * FROM records")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        'records.html',
        records=data,
        search=search
    )


# ==========================================
# Delete Record Module
# Removes selected record from database
# ==========================================

@app.route('/delete/<int:id>')
def delete_record(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM records WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/records')


# ==========================================
# Duplicate Logs Module
# Displays all duplicate attempts
# ==========================================
@app.route('/logs')
def logs():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM duplicate_logs
        ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return render_template(
        'logs.html',
        logs=logs
    )


# ==========================================
# Dashboard Analytics Module
# Displays project statistics
# ==========================================
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Total Records
    cursor.execute("SELECT COUNT(*) FROM records")
    total_records = cursor.fetchone()[0]

    # Total Duplicate Attempts
    cursor.execute("SELECT COUNT(*) FROM duplicate_logs")
    total_duplicates = cursor.fetchone()[0]

    # Duplicate Emails
    cursor.execute("""
        SELECT COUNT(*)
        FROM duplicate_logs
        WHERE duplicate_type='Email'
    """)
    duplicate_emails = cursor.fetchone()[0]

    # Duplicate Phones
    cursor.execute("""
        SELECT COUNT(*)
        FROM duplicate_logs
        WHERE duplicate_type='Phone'
    """)
    duplicate_phones = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_records=total_records,
        total_duplicates=total_duplicates,
        duplicate_emails=duplicate_emails,
        duplicate_phones=duplicate_phones
    )


if __name__ == '__main__':
    app.run(debug=True)
