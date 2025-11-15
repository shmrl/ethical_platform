from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = "super_secret_key"

init_db()

# ---- Home ----
@app.route("/")
def home():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(debug=True)
