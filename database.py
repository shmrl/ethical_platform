import sqlite3

def init_db():
    conn = sqlite3.connect("reports.db")
    c = conn.cursor()

    # ---- Reports table ----
    c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        characteristics TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ---- Leadership accounts ----
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
    except sqlite3.IntegrityError:
        pass

    # ---- Company info table ----
    c.execute("""
    CREATE TABLE IF NOT EXISTS company_info (
        id INTEGER PRIMARY KEY,
        motto TEXT,
        standards TEXT,
        characteristics TEXT
    );
    """)

    # Initialize a row if none exists
    c.execute("SELECT COUNT(*) FROM company_info WHERE id=1")
    if c.fetchone()[0] == 0:
        c.execute("""
        INSERT INTO company_info (id, motto, standards, characteristics)
        VALUES (?, ?, ?, ?)
        """, (1, "Your Company Motto Here", "Excellence, Integrity, Accountability", "Integrity, Excellence, Teamwork"))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
