from contextlib import closing

from database.database import get_connection
from models.subject import Subject


def get_all() -> list[Subject]:
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT subject_id, name FROM subjects ORDER BY subject_id").fetchall()
    return [Subject(*row) for row in rows]


def get_by_id(subject_id: int) -> Subject | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT subject_id, name FROM subjects WHERE subject_id = ?", (subject_id,)
        ).fetchone()
    return Subject(*row) if row else None


def create(name):
    with closing(get_connection()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO subjects (name) VALUES (?)",
            (name,),
        )
        return cursor.lastrowid


def update(subject_id, name):
    with closing(get_connection()) as conn, conn:
        conn.execute(
            "UPDATE subjects SET name = ? WHERE subject_id = ?",
            (name, subject_id),
        )


def delete(subject_id: int):
    with closing(get_connection()) as conn, conn:
        conn.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))

