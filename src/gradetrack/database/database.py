import sqlite3
from contextlib import closing
from pathlib import Path

DATABASE_DIR = Path(__file__).parent
DB_FILE = DATABASE_DIR.parents[2] / "gradetrack.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database():
    with closing(get_connection()) as conn:
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'users'"
        ).fetchone()
        if not exists:
            conn.executescript((DATABASE_DIR / "schema.sql").read_text(encoding="utf-8"))
