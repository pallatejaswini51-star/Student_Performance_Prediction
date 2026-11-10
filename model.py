
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "student_performance.csv")
MODEL_PATH = os.path.join(BASE_DIR, "student_model.pkl")


def train_model():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    features = [
        "Attendance",
        "StudyHours",
        "InternalMarks",
        "AssignmentMarks",
        "PreviousMarks"
    ]
    target = "FinalMarks"

    required_columns = features + [target]
    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing dataset columns: {missing}"
        )

    data = data[required_columns].apply(
        pd.to_numeric, errors="coerce"
    ).dropna()

    if len(data) < 5:
        raise ValueError(
            "At least 5 valid dataset rows are required."
        )

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully!")
    print(f"R² score: {r2:.3f}")
    print(f"Mean absolute error: {mae:.2f} marks")

    return model


if __name__ == "__main__":
    train_model()
