# Student Marks Management System

## Problem Statement
In many colleges, student marks are stored in Excel or on paper, and teachers manually calculate averages and identify weak students. This is time-consuming and error-prone.

## Solution
A web-based system that:
- Stores marks in a SQLite database
- Automatically calculates averages
- Generates performance analysis reports
- Identifies weak students automatically

## Technology Stack
- **Backend**: Python with Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap, Chart.js

## Features
1. Student Management (Add/View students)
2. Subject Management (Add/View subjects)
3. Marks Entry (Enter marks for students in each subject)
4. Automatic Average Calculation
5. Performance Reports (Individual student & subject-wise)
6. Weak Student Identification (Below threshold alerts)

## How to Run
1. Install Flask: `pip install flask`
2. Run the app: `python app.py`
3. Open browser: `http://localhost:5000`

## Project Structure
```
/performance
├── app.py              # Main Flask application
├── database.py         # Database setup and models
├── data.sql           # Database schema
├── static/
│   └── style.css      # Custom styles
└── templates/
    ├── base.html      # Base template
    ├── index.html     # Home page
    ├── students.html  # Student management
    ├── subjects.html  # Subject management
    ├── marks.html     # Marks entry
    └── reports.html   # Performance reports
