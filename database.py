import sqlite3

def init_db():
    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    # Table for anonymous reports
    c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Leadership accounts
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # Default admin account (username: admin, password: admin123)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  ("admin", "admin123"))
    except:
        pass

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
