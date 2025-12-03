from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Initialize database
init_db()

# Hardcoded manager credentials
MANAGER_USERNAME = "manager1"
MANAGER_PASSWORD = "company2025"

# ---- Home ----
@app.route("/")
def home():
    conn = sqlite3.connect("reports.db")
    c = conn.cursor()
    c.execute("SELECT motto, standards, characteristics FROM company_info WHERE id=1")
    row = c.fetchone()
    motto, standards, characteristics = row
    conn.close()
    return render_template("index.html",
        motto=motto,
        standards=standards,
        characteristics=characteristics)


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
        username = request.form.get("username")
        password = request.form.get("password")

        if username == MANAGER_USERNAME and password == MANAGER_PASSWORD:
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

# ---- View Company Standards ----
@app.route("/standards")
def standards():
    conn = sqlite3.connect("reports.db")
    c = conn.cursor()
    c.execute("SELECT standards FROM company_info WHERE id=1")
    standards = c.fetchone()[0]
    conn.close()
    return render_template("standards.html", standards=standards)

# ---- View Company Characteristics ----
@app.route("/characteristics")
def characteristics():
    conn = sqlite3.connect("reports.db")
    c = conn.cursor()
    c.execute("SELECT characteristics FROM company_info WHERE id=1")
    characteristics = c.fetchone()[0]
    conn.close()
    return render_template("characteristics.html", characteristics=characteristics)


# ---- Edit Company Standards ----
@app.route("/edit_standards", methods=["GET", "POST"])
def edit_standards():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    if request.method == "POST":
        new_standards = request.form["standards"]
        c.execute("UPDATE company_info SET standards=? WHERE id=1", (new_standards,))
        conn.commit()
        conn.close()
        return redirect("/standards")

    c.execute("SELECT standards FROM company_info WHERE id=1")
    standards = c.fetchone()[0]
    conn.close()
    return render_template("edit_standards.html", standards=standards)

if __name__ == "__main__":
    app.run(debug=True)
