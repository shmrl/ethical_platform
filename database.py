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

    # --- New table for company info ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS company_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        motto TEXT,
        characteristics TEXT
    );
    """)

    # Initialize a row if none exists
    c.execute("SELECT COUNT(*) FROM company_info")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO company_info (motto, characteristics) VALUES (?, ?)",
                  ("Your Company Motto Here", "Integrity, Excellence, Teamwork"))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
