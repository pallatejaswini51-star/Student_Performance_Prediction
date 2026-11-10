import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, "database", "student.db")

MODEL = os.path.join(BASE_DIR, "student_model.pkl")

SECRET_KEY = "student_prediction_2026"