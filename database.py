
import sqlite3
import os

# Database file location
DB_FOLDER = "database"
DB_PATH = os.path.join(DB_FOLDER, "student.db")


def get_connection():
    os.makedirs(DB_FOLDER, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Existing predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attendance REAL,
            study_hours REAL,
            internal_marks REAL,
            assignment_marks REAL,
            previous_marks REAL,
            result TEXT
        )
    """)

    # New users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(attendance, study_hours, internal_marks,
                    assignment_marks, previous_marks, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (attendance, study_hours, internal_marks,
         assignment_marks, previous_marks, result)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        attendance,
        study_hours,
        internal_marks,
        assignment_marks,
        previous_marks,
        result
    ))

    conn.commit()
    conn.close()


def get_all_predictions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    records = cursor.fetchall()

    conn.close()
    return records


def get_total_predictions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    conn.close()
    return total

def delete_prediction(prediction_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM predictions WHERE id = ?",
        (prediction_id,)
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted
