import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initial available seats per course
seats = {
    "Computer Science": 3,
    "Electronics & Communication": 2,
    "Mechanical Engineering": 2,
    "Data Science & AI": 1
}

# Previous college students' achievements per field
achievements_data = {
    "Computer Science": [
        {"name": "Aarav Sharma (Batch 2024)", "achievement": "Placed at Google as Software Engineer with ₹42 LPA package."},
        {"name": "Sneha Nair (Batch 2023)", "achievement": "1st Place Winner at Smart India Hackathon (National Finals)."},
        {"name": "Rohan Verma (Batch 2025)", "achievement": "Published open-source cloud security tool used by 15,000+ developers."}
    ],
    "Electronics & Communication": [
        {"name": "Kavya Rao (Batch 2024)", "achievement": "Designed an award-winning low-power IoT chip at Texas Instruments."},
        {"name": "Vikram Hegde (Batch 2023)", "achievement": "Selected for ISRO satellite communication research internship."},
        {"name": "Ananya Kulkarni (Batch 2025)", "achievement": "Gold Medalist in National Robotics & Embedded Systems Championship."}
    ],
    "Mechanical Engineering": [
        {"name": "Karthik Gowda (Batch 2024)", "achievement": "Built an electric formula race car that won 2nd place at SAE Supra."},
        {"name": "Divya Menon (Batch 2023)", "achievement": "Lead Design Engineer at Mahindra Electric Vehicle R&D Division."},
        {"name": "Siddharth Joshi (Batch 2025)", "achievement": "Patented a high-efficiency solar thermal water desalination unit."}
    ],
    "Data Science & AI": [
        {"name": "Meera Krishnan (Batch 2024)", "achievement": "Kaggle Master & AI Research Fellow at Microsoft Research India."},
        {"name": "Rahul Bhat (Batch 2023)", "achievement": "Developed an early crop-disease detection AI app used by 50,000 farmers."},
        {"name": "Neha Patil (Batch 2025)", "achievement": "Best Paper Award at International Conference on Machine Learning."}
    ]
}

@app.route("/", methods=["GET", "POST"])
def index():
    status = None
    message = None

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        course = request.form.get("course")
        pu_percentage_raw = request.form.get("pu_percentage", "").strip()

        try:
            pu_percentage = float(pu_percentage_raw)
        except ValueError:
            pu_percentage = -1

        if not student_name or not course or pu_percentage < 0 or pu_percentage > 100:
            status = "error"
            message = "Please enter valid details and a PU percentage between 0 and 100."
        elif pu_percentage > 80:
            # Deny admission and show as an error message (no seat deducted, no redirect)
            status = "error"
            message = f"Hi {student_name} ({pu_percentage}%), you are a good knowledge person and potential person, don't spoil your future here."
        else:
            # Only students with 80% or below enter the random selection
            decision = random.choice(["success", "failed"])

            if decision == "success" and seats.get(course, 0) > 0:
                seats[course] -= 1
                return redirect(url_for("achievements", name=student_name, course=course, percentage=pu_percentage))
            else:
                status = "error"
                message = f"Admission Failed due to no seat availability in {course}. Better luck next time!"

    return render_template("index.html", seats=seats, status=status, message=message)

@app.route("/achievements")
def achievements():
    student_name = request.args.get("name", "Student")
    course = request.args.get("course", "Computer Science")
    percentage = request.args.get("percentage", "")
    course_achievements = achievements_data.get(course, [])

    return render_template(
        "achievements.html",
        student_name=student_name,
        course=course,
        percentage=percentage,
        achievements=course_achievements
    )

if __name__ == "__main__":
    app.run(debug=True)