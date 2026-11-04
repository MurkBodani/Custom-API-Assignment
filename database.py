
import sqlite3

DATABASE_NAME = "students.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Student database created successfully!")
