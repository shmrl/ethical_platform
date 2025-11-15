from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Initialize the database and tables
init_db()

# ---- Home ----
@app.route("/")
def home():
    # Fetch motto from DB to display on home page
    conn = sqlite3.connect("reports.db")
    c = conn.cursor()
    c.execute("SELECT motto FROM company_info WHERE id=1")
    motto = c.fetchone()[0]
    conn.close()
    return render_template("index.html", motto=motto)

# ---- Anonymous Report Submission ----
@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        issue = request.form["issue"]

        conn = sqlite3.connect("reports.db")
        c = conn.cursor()
        c.execute("INSERT INTO reports (issue) VALUES (?)", (issue,))
        conn.commit()
        conn.close()

        return redirect("/submitted")

    return render_template("report.html")

@app.route("/submitted")
def submitted():
    return render_template("submitted.html")

# ---- Leadership Login ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("reports.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials.")

    return render_template("login.html")

# ---- Dashboard ----
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reports ORDER BY created_at DESC")
    reports = c.fetchall()
    conn.close()

    return render_template("dashboard.html", reports=reports)

# ---- Logout ----
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---- Edit Company Motto ----
@app.route("/edit_motto", methods=["GET", "POST"])
def edit_motto():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    if request.method == "POST":
        new_motto = request.form["motto"]
        c.execute("UPDATE company_info SET motto=? WHERE id=1", (new_motto,))
        conn.commit()
        conn.close()
        return redirect("/")

    c.execute("SELECT motto FROM company_info WHERE id=1")
    motto = c.fetchone()[0]
    conn.close()
    return render_template("edit_motto.html", motto=motto)

# ---- Edit Company Characteristics ----
@app.route("/edit_characteristics", methods=["GET", "POST"])
def edit_characteristics():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    if request.method == "POST":
        new_chars = request.form["characteristics"]
        c.execute("UPDATE company_info SET characteristics=? WHERE id=1", (new_chars,))
        conn.commit()
        conn.close()
        return redirect("/characteristics")

    c.execute("SELECT characteristics FROM company_info WHERE id=1")
    characteristics = c.fetchone()[0]
    conn.close()
    return render_template("edit_characteristics.html", characteristics=characteristics)

# ---- View Company Characteristics ----
@app.route("/characteristics")
def characteristics():
    # Fetch characteristics from DB to display on characteristics.html
    conn = sqlite3.connect("reports.db")
    c = conn.cursor()
    c.execute("SELECT characteristics FROM company_info WHERE id=1")
    characteristics = c.fetchone()[0]
    conn.close()
    return render_template("characteristics.html", characteristics=characteristics)


if __name__ == "__main__":
    app.run(debug=True)
