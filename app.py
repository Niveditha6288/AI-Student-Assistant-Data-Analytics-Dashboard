from flask import Flask, render_template, request, redirect, session
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = "eduai_secret_key"

# Load dataset
if os.path.exists("data/students.csv"):
    students = pd.read_csv("data/students.csv")
elif os.path.exists("students.csv"):
    students = pd.read_csv("students.csv")
else:
    students = pd.DataFrame([{
        "Student_ID": 1216,
        "Name": "Priya216",
        "Branch": "CSE",
        "Semester": 3,
        "Attendance": 71,
        "Python": 47,
        "DBMS": 89,
        "DSA": 81,
        "Assignments": 8,
        "Previous_GPA": 8.2
    }])

# Load ML model
model = None

try:
    model = joblib.load("student_model.pkl")
except:
    pass


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        student_id = request.form.get("student_id")
        password = request.form.get("password")

        # Demo password
        if password != "1234":
            return render_template(
                "login.html",
                error="Invalid password. Use 1234 for demo."
            )

        try:
            student_id = int(student_id)
        except:
            return render_template(
                "login.html",
                error="Enter a valid Student ID."
            )

        student = students[students["Student_ID"] == student_id]

        if student.empty:
            return render_template(
                "login.html",
                error="Student ID not found."
            )

        session["student_id"] = student_id

        return redirect("/")

    return render_template("login.html")


# DASHBOARD
@app.route("/")
def dashboard():

    if "student_id" not in session:
        return redirect("/login")

    student_id = session["student_id"]

    student_data = students[
        students["Student_ID"] == student_id
    ]

    if student_data.empty:
        return redirect("/login")

    student = student_data.iloc[0]

    average = (
        student["Python"] +
        student["DBMS"] +
        student["DSA"]
    ) / 3

    prediction = "B"

    if model is not None:
        try:

            input_data = pd.DataFrame([{
                "Attendance": student["Attendance"],
                "Python": student["Python"],
                "DBMS": student["DBMS"],
                "DSA": student["DSA"],
                "Assignments": student["Assignments"],
                "Previous_GPA": student["Previous_GPA"]
            }])

            prediction = model.predict(input_data)[0]

        except:
            prediction = "B"

    recommendations = []

    if student["Python"] < 60:
        recommendations.append(
            "Improve Python fundamentals."
        )

    if student["DBMS"] < 60:
        recommendations.append(
            "Revise DBMS concepts regularly."
        )

    if student["DSA"] < 60:
        recommendations.append(
            "Practice DSA problems daily."
        )

    if student["Attendance"] < 75:
        recommendations.append(
            "Improve your attendance."
        )

    if not recommendations:
        recommendations.append(
            "Maintain your current performance."
        )

    return render_template(
        "dashboard.html",
        student_name=student["Name"],
        average=round(average, 2),
        attendance=student["Attendance"],
        prediction=prediction,
        semester=student["Semester"],
        python=student["Python"],
        dbms=student["DBMS"],
        dsa=student["DSA"],
        previous_gpa=student["Previous_GPA"],
        recommendations=recommendations
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
@app.route("/performance")
def performance():

    student = students.iloc[0]

    average = (
        student["Python"] +
        student["DBMS"] +
        student["DSA"]
    ) / 3

    prediction = "B"

    if model is not None:
        try:

            input_data = pd.DataFrame([{
                "Attendance": student["Attendance"],
                "Python": student["Python"],
                "DBMS": student["DBMS"],
                "DSA": student["DSA"],
                "Assignments": student["Assignments"],
                "Previous_GPA": student["Previous_GPA"]
            }])

            prediction = model.predict(input_data)[0]

        except Exception:
            prediction = "B"

    return render_template(
        "performance.html",
        python=student["Python"],
        dbms=student["DBMS"],
        dsa=student["DSA"],
        average=round(average, 2),
        prediction=prediction
    )

@app.route("/analytics")
def analytics():

    total_students = len(students)

    avg_python = round(students["Python"].mean(), 2)
    avg_dbms = round(students["DBMS"].mean(), 2)
    avg_dsa = round(students["DSA"].mean(), 2)

    average_attendance = round(
        students["Attendance"].mean(), 2
    )

    students["Average"] = (
        students["Python"] +
        students["DBMS"] +
        students["DSA"]
    ) / 3

    passed = int((students["Average"] >= 50).sum())
    failed = total_students - passed

    pass_percentage = round(
        (passed / total_students) * 100, 2
    )

    at_risk = int(
        ((students["Average"] < 50) |
         (students["Attendance"] < 75)).sum()
    )

    return render_template(
        "analytics.html",
        total_students=total_students,
        avg_python=avg_python,
        avg_dbms=avg_dbms,
        avg_dsa=avg_dsa,
        average_attendance=average_attendance,
        passed=passed,
        failed=failed,
        pass_percentage=pass_percentage,
        at_risk=at_risk
    )

@app.route("/attendance")
def attendance():

    student = students.iloc[0]

    return render_template(
        "attendance.html",
        attendance=student["Attendance"]
    )
@app.route("/profile")
def profile():

    student = students.iloc[0]

    return render_template(
        "profile.html",
        student_id=student["Student_ID"],
        student_name=student["Name"],
        branch=student["Branch"],
        semester=student["Semester"],
        previous_gpa=student["Previous_GPA"],
        attendance=student["Attendance"]
    )
@app.route("/ai-assistant")
def ai_assistant():

    student = students.iloc[0]

    average = (
        student["Python"] +
        student["DBMS"] +
        student["DSA"]
    ) / 3

    prediction = "B"

    if model is not None:
        try:

            input_data = pd.DataFrame([{
                "Attendance": student["Attendance"],
                "Python": student["Python"],
                "DBMS": student["DBMS"],
                "DSA": student["DSA"],
                "Assignments": student["Assignments"],
                "Previous_GPA": student["Previous_GPA"]
            }])

            prediction = model.predict(input_data)[0]

        except Exception:
            prediction = "B"


    recommendations = []

    if student["Python"] < 60:
        recommendations.append(
            "Improve Python fundamentals."
        )

    if student["DBMS"] < 60:
        recommendations.append(
            "Revise DBMS concepts regularly."
        )

    if student["DSA"] < 60:
        recommendations.append(
            "Practice DSA problems daily."
        )

    if student["Attendance"] < 75:
        recommendations.append(
            "Improve your attendance."
        )

    if not recommendations:
        recommendations.append(
            "Maintain your current performance."
        )


    return render_template(
        "ai_assistant.html",
        prediction=prediction,
        python=student["Python"],
        dbms=student["DBMS"],
        dsa=student["DSA"],
        attendance=student["Attendance"],
        average=round(average, 2),
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(debug=True)