from flask import Flask, render_template_string, request

app = Flask(__name__)

def validate_input(absences, prelim_exam, quizzes, requirements, recitation):
    errors = []
    try:
        absences = int(absences)
        if absences < 0:
            errors.append("Absences must be 0 or greater.")
    except ValueError:
        errors.append("Absences must be an integer.")

    for name, value in [
        ("Prelim Exam Grade", prelim_exam),
        ("Quizzes Grade", quizzes),
        ("Requirements Grade", requirements),
        ("Recitation Grade", recitation),
    ]:
        try:
            val = float(value)
            if not (0 <= val <= 100):
                errors.append(f"{name} must be between 0 and 100.")
        except ValueError:
            errors.append(f"{name} must be a number.")
    return errors

def attendance_score(absences):
    if absences >= 4:
        return 0, True  # 0 attendance, failed due to absences
    else:
        return max(0, 100 - absences * 10), False

def class_standing(quizzes, requirements, recitation):
    return quizzes * 0.4 + requirements * 0.3 + recitation * 0.3

def prelim_grade(prelim_exam, attendance, class_stand):
    return prelim_exam * 0.6 + attendance * 0.1 + class_stand * 0.3

def required_grades(prelim, target):
    x = (target - 0.2 * prelim) / 0.8
    if x < 0: x = 0
    if x > 100: x = 100
    return round(x, 2), round(x, 2)

index_template = '''
<!doctype html>
<html>
<head>
    <title>Prelim Exam Calculator</title>
    <style>
        .logo {
                position: fixed;
                top: 0px;
                height: auto;
                width: 100%;
                background-color: white;
                text-align: left;
        }
        img {
                height: 40px;
                width: auto;
                margin: 4px -6px;
        }
        .container1 {
                position: fixed;
                top: 2px;
                middle: 320px;
                height: auto;
                width: 100%;
        }
        h1 { 
                text-align: center;
                background: maroon;
                color: white;
                font-style: italic;
                font-size: 70px;
        }
        body {
                font-family: Arial, sans-serif;
                background-image: url('https://farm5.staticflickr.com/4652/40100486212_8a50eef2ee_o.jpg');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                margin: 0;
                padding: 0;
                text-align: center;
        }
        .container2 {
                margin: 210px 0 0 290px;
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                text-align: center;
        }
        form {
                background: maroon;
                padding: 30px 40px;
                border-radius: 10px;
                box-shadow: 0 0 10px #aaa;
                color: white;
                text-align: left;
                display: block;
                box-sizing: border-box;
                width: 330px;
                height: 410px;
                align-items: center;
                text-align: center;
                line-height: 1.9;
        }
        input[type="number"] {
                font-size: 1em;
                margin: -2px;
                padding: 5px;
                width: 60%;
        }
        input[name="prelim_exam"] {
                width: 32.5%;
        }
        input[name="quizzes"] {
                width: 46%;
        }
        input[name="requirements"] {
                width: 29.6%;
        }
        input[name="recitation"] {
                width: 41%;
        }
        .1, .2, .3, .4, .5 {
                text-align: left;
        }
        input[type="submit"] {
                font-size: 1em;
                padding: 8px 20px;
                margin-top: 10px;
        }
        .error {
                color: red;
        }
        .container3 {
                margin: -411px 0 0 400px;
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                line-height: 1.4;
        }
        .result {
                background: maroon;
                padding: 30px 40px;
                border-radius: 10px;
                box-shadow: 0 0 10px #aaa;
                color: white;
                text-align: center;
                display: block;
                box-sizing: border-box;
                width: 330px;
                height: 410px;
        }
        form label {
                display: block;
                text-align: left;
                width: 100%;
        }
        .pass, .dl, .pr {
                text-align: center;
                margin-top: 10px;
        }
        .mfn1, .mfn2 {
                font-style: italic;
        }
        .r2, .r3 {
                color: goldenrod;
                width: 150px;
                height: 20px;
                text-align: center;
                margin-left: 50px;
        }
        r1 {
                color: goldenrod;
        }
    </style>
</head>
<body>
    <div class="logo">
    <img src="https://perpetualdalta.edu.ph/new/wp-content/uploads/2025/01/UNIVERSITY-OF-PERPETUAL-HELP-SYSTEM-DALTA-Long-MOL-Campus-768x71.png"
         alt="Logo">
    </div>
    <div class="container1">
        <h1>Prelim Grade Calculator</h1>
    </div>
    <div class="container2">
        <form method="post">
            <label class="1">Absences:
                <input type="number" name="absences" min="0" required
                value="{{ request.form.absences or '' }}">
            </label><br>
            <label class="2">Prelim Exam Grade:
                <input type="number" name="prelim_exam" min="0" max="100" required
                value="{{ request.form.prelim_exam or '' }}">
            </label><br>
            <label class="3">Quizzes Grade:
                <input type="number" name="quizzes" min="0" max="100" required
                value="{{ request.form.quizzes or '' }}">
            </label>
            <label class="4">Requirements Grade:
                <input type="number" name="requirements" min="0" max="100" required
                value="{{ request.form.requirements or '' }}">
            </label><br>
            <label class="5">Recitation Grade:
                <input type="number" name="recitation" min="0" max="100" required
                value="{{ request.form.recitation or '' }}">
            </label><br>
            <input type="submit" value="Calculate">
        </form>
        {% if errors %}
            <div class="error">
                <ul>
                {% for error in errors %}
                    <li>{{ error }}</li>
                {% endfor %}
                </ul>
            </div>
        {% endif %}
        {% if result %}
            <div class ="container3">
                <div class="result">
                    <p class="pr">
                        Prelim Grade: <r1><strong>{{ result.prelim_grade }}</strong></r2>
                    </p><br>
                    {% if result.pass_pair %}
                        <p class="pass">
                                To PASS (75):
                            <p class="mfn1">Midterm & Final grades needed:</p>
                            <p class="r2">
                                <strong>{{ result.pass_pair[0] }}</strong> and
                                <strong>{{ result.pass_pair[1] }}</strong>
                            </p>
                        </p><br>
                    {% endif %}
                    {% if result.deans_pair %}
                        <p class="dl">
                                To qualify for Dean's List (90):<br>
                            <p class="mfn2">Midterm & Final grades needed:</p>
                            <p class="r3">
                                <strong>{{ result.deans_pair[0] }}</strong> and
                                <strong>{{ result.deans_pair[1] }}</strong>
                            </p>
                        </p>
                    {% endif %}
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    errors = []
    if request.method == "POST":
        absences = request.form.get("absences", "")
        prelim_exam = request.form.get("prelim_exam", "")
        quizzes = request.form.get("quizzes", "")
        requirements = request.form.get("requirements", "")
        recitation = request.form.get("recitation", "")

        errors = validate_input(absences, prelim_exam, quizzes, requirements, recitation)
        if not errors:
            absences = int(absences)
            prelim_exam = float(prelim_exam)
            quizzes = float(quizzes)
            requirements = float(requirements)
            recitation = float(recitation)

            attendance, failed = attendance_score(absences)
            if failed:
                result = {
                    "prelim_grade": "FAILED (4 or more absences)",
                    "pass_pair": None,
                    "deans_pair": None,
                }
            else:
                class_stand = class_standing(quizzes, requirements, recitation)
                prelim = prelim_grade(prelim_exam, attendance, class_stand)
                pass_pair = required_grades(prelim, 75)
                deans_pair = required_grades(prelim, 90)
                result = {
                    "prelim_grade": round(prelim, 2),
                    "pass_pair": pass_pair,
                    "deans_pair": deans_pair
                }
    return render_template_string(index_template, result=result, errors=errors, request=request)


if __name__ == "__main__":

    app.run(debug=True)

