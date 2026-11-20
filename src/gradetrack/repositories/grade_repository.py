from contextlib import closing

from database.database import get_connection
from models.grade import Grade


def get_all() -> list[Grade]:
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT grade_id, student_id, subject_id, value, grade_date FROM grades ORDER BY grade_id").fetchall()
    return [Grade(*row) for row in rows]


def get_by_id(grade_id: int) -> Grade | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT grade_id, student_id, subject_id, value, grade_date FROM grades WHERE grade_id = ?", (grade_id,)
        ).fetchone()
    return Grade(*row) if row else None


def create(student_id, subject_id, value, grade_date):
    with closing(get_connection()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO grades (student_id, subject_id, value, grade_date) VALUES (?, ?, ?, ?)",
            (student_id, subject_id, value, grade_date,),
        )
        return cursor.lastrowid


def update(grade_id, student_id, subject_id, value, grade_date):
    with closing(get_connection()) as conn, conn:
        conn.execute(
            "UPDATE grades SET student_id = ?, subject_id = ?, value = ?, grade_date = ? WHERE grade_id = ?",
            (student_id, subject_id, value, grade_date, grade_id),
        )


def delete(grade_id: int):
    with closing(get_connection()) as conn, conn:
        conn.execute("DELETE FROM grades WHERE grade_id = ?", (grade_id,))


def get_for_export(student_id=None):
    query = """
        SELECT g.grade_id, g.value, g.grade_date,
               u.user_id, u.full_name, gr.group_id, gr.name,
               s.subject_id, s.name
        FROM grades AS g
        JOIN users AS u ON u.user_id = g.student_id
        LEFT JOIN groups AS gr ON gr.group_id = u.group_id
        JOIN subjects AS s ON s.subject_id = g.subject_id
    """
    parameters = ()
    if student_id is not None:
        query += " WHERE g.student_id = ?"
        parameters = (student_id,)
    query += " ORDER BY g.grade_id"
    with closing(get_connection()) as conn:
        rows = conn.execute(query, parameters).fetchall()
    return [
        {
            "grade_id": row[0],
            "value": row[1],
            "grade_date": row[2],
            "student": {
                "user_id": row[3],
                "full_name": row[4],
                "group": {"group_id": row[5], "name": row[6]},
            },
            "subject": {"subject_id": row[7], "name": row[8]},
        }
        for row in rows
    ]

