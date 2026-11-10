# Student Performance Prediction System

## Project Overview

The Student Performance Prediction System is a machine learning-based web application that predicts students' academic performance using their attendance, study hours, internal marks, assignment marks, and previous marks.

The application helps users understand predicted student performance through a simple web interface.

## Technologies Used

- **Programming Language:** Python
- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Flask
- **Machine Learning:** Scikit-learn
- **Database:** SQLite
- **Model:** Random Forest Regressor

## Features

- User registration and login
- Student performance prediction
- Prediction history
- Dashboard with performance statistics
- Analytics page
- Delete individual prediction records

## Project Structure

```text
Student_Performance_Prediction/
├── app.py
├── database.py
├── model.py
├── utils.py
├── config.py
├── requirements.txt
├── README.md
├── student_model.pkl
├── database/
├── static/
│   └── css/
└── templates/
```

## Input Features

The system uses the following inputs:

1. Attendance
2. Study Hours
3. Internal Marks
4. Assignment Marks
5. Previous Marks

## How to Run the Project

1. Install Python on your computer.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Install the required packages:

   `pip install -r requirements.txt`

5. Start the application:

   `python app.py`

6. Open your browser and visit:

   `http://127.0.0.1:5000`

7. Register or log in to use the application.

## Database

SQLite is used to store user details and prediction history. The database is created and managed by the application.

## Project Objective

The main objective is to demonstrate how machine learning can be integrated into a web application to predict student performance based on academic information.
