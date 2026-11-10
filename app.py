
from database import (
    create_table,
    save_prediction,
    get_total_predictions,
    get_all_predictions,
    get_connection,
    delete_prediction
)

import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from utils import get_performance
from database import (
    create_table,
    get_connection,
    save_prediction,
    get_total_predictions,
    get_all_predictions
)

app = Flask(__name__)
app.secret_key = "student-performance-project-key"

# Create database tables
create_table()


# HOME
@app.route("/")
def home():
    return render_template("index.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not name or not username or not password:
            return render_template(
                "register.html",
                error="Please fill in all fields."
            )

        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters."
            )

        conn = get_connection()

        try:
            cursor = conn.cursor()
            password_hash = generate_password_hash(password)

            cursor.execute(
                """
                INSERT INTO users (name, username, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, username, password_hash)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="Username already exists. Please choose another."
            )

        finally:
            conn.close()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_connection()

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, username, password_hash
                FROM users
                WHERE username = ?
                """,
                (username,)
            )
            user = cursor.fetchone()

        finally:
            conn.close()

        if user and check_password_hash(user[3], password):
            session.clear()
            session["logged_in"] = True
            session["user_id"] = user[0]
            session["username"] = user[2]
            session["name"] = user[1]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# PREDICT
@app.route("/predict", methods=["POST"])
def predict():
    if not session.get("logged_in"):
        return redirect("/login")

    try:
        attendance = float(request.form["attendance"])
        study_hours = float(request.form["study_hours"])
        internal_marks = float(request.form["internal_marks"])
        assignment_marks = float(request.form["assignment_marks"])
        previous_marks = float(request.form["previous_marks"])

        if not 0 <= attendance <= 100:
            raise ValueError("Attendance must be between 0 and 100.")

        if not 0 <= study_hours <= 24:
            raise ValueError("Study hours must be between 0 and 24.")

        for name, value in [
            ("Internal marks", internal_marks),
            ("Assignment marks", assignment_marks),
            ("Previous marks", previous_marks)
        ]:
            if not 0 <= value <= 100:
                raise ValueError(
                    f"{name} must be between 0 and 100."
                )

        result = get_performance(
            attendance,
            study_hours,
            internal_marks,
            assignment_marks,
            previous_marks
        )

        if not isinstance(result, dict) or "category" not in result:
            return render_template(
                "index.html",
                error="Prediction result is unavailable. Please check the ML model."
            )

        save_prediction(
            attendance,
            study_hours,
            internal_marks,
            assignment_marks,
            previous_marks,
            result["category"]
        )

        return render_template("result.html", result=result)

    except (ValueError, TypeError) as error:
        return render_template("index.html", error=str(error))

    except KeyError:
        return render_template(
            "index.html",
            error="Please fill in all required fields."
        )


# HISTORY (SHARED BY ALL USERS)
@app.route("/history")
def history():
    if not session.get("logged_in"):
        return redirect("/login")

    records = get_all_predictions()

    return render_template(
        "history.html",
        records=records
    )

@app.route("/delete_prediction/<int:prediction_id>", methods=["POST"])
def delete_prediction_route(prediction_id):
    if not session.get("logged_in"):
        return redirect("/login")

    delete_prediction(prediction_id)

    return redirect("/history")



# DASHBOARD (SHARED BY ALL USERS)
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")

    total = get_total_predictions()
    records = get_all_predictions()

    category_counts = {
        "Excellent": 0,
        "Very Good": 0,
        "Good": 0,
        "Average": 0,
        "Needs Improvement": 0
    }

    for record in records:
        category = record[6]
        if category in category_counts:
            category_counts[category] += 1

    return render_template(
        "dashboard.html",
        total=total,
        records=records,
        category_counts=category_counts
    )


# ANALYTICS (SHARED BY ALL USERS)
@app.route("/analytics")
def analytics():
    if not session.get("logged_in"):
        return redirect("/login")

    records = get_all_predictions()

    category_counts = {
        "Excellent": 0,
        "Very Good": 0,
        "Good": 0,
        "Average": 0,
        "Needs Improvement": 0
    }

    for record in records:
        category = record[6]
        if category in category_counts:
            category_counts[category] += 1

    return render_template(
        "analytics.html",
        records=records,
        total=len(records),
        category_counts=category_counts
    )


if __name__ == "__main__":
    app.run(debug=True)
