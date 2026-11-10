
import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "student_model.pkl")

model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
except Exception as error:
    print("Could not load the student model:", error)


def get_performance(
    attendance,
    study_hours,
    internal_marks,
    assignment_marks,
    previous_marks
):
    if model is None:
        raise RuntimeError(
            "Model not found. Please train model.py first."
        )

    features = [[
        attendance,
        study_hours,
        internal_marks,
        assignment_marks,
        previous_marks
    ]]

    predicted_marks = float(model.predict(features)[0])
    predicted_marks = max(0.0, min(100.0, predicted_marks))

    if predicted_marks >= 90:
        category = "Excellent"
    elif predicted_marks >= 75:
        category = "Very Good"
    elif predicted_marks >= 60:
        category = "Good"
    elif predicted_marks >= 40:
        category = "Average"
    else:
        category = "Needs Improvement"

    return {
        "marks": round(predicted_marks, 2),
        "category": category
    }
