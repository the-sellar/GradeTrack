import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).parent
DB_FILE = DATABASE_DIR.parents[2] / "gradetrack.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database():
    conn = get_connection()
    conn.executescript((DATABASE_DIR / "schema.sql").read_text(encoding="utf-8"))
    conn.close()


def print_tables():
    conn = get_connection()
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY rowid"
    ).fetchall()

    for (name,) in tables:
        cursor = conn.execute(f"SELECT * FROM {name}")
        rows = cursor.fetchall()

        print(f"\n{name} - записей: {len(rows)}")
        print(" | ".join(column[0] for column in cursor.description))
        for row in rows:
            print(" | ".join(str(value)[:30] for value in row))

    conn.close()
