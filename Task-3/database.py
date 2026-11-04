import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "authentication.db"


def create_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    users = [
        ("student", "student123", "Student"),
        ("employee", "employee123", "Employee"),
        ("admin", "admin123", "Admin")
    ]

    for username, password, role in users:
        hashed_password = generate_password_hash(password)

        conn.execute("""
            INSERT OR IGNORE INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, (username, hashed_password, role))

    conn.commit()
    conn.close()

    print("Authentication database created successfully!")


if __name__ == "__main__":
    create_database()