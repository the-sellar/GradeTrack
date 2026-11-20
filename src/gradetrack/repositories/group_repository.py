from contextlib import closing

from database.database import get_connection
from models.group import Group


def get_all() -> list[Group]:
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT group_id, name FROM groups ORDER BY group_id").fetchall()
    return [Group(*row) for row in rows]


def get_by_id(group_id: int) -> Group | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT group_id, name FROM groups WHERE group_id = ?", (group_id,)
        ).fetchone()
    return Group(*row) if row else None


def create(name):
    with closing(get_connection()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO groups (name) VALUES (?)",
            (name,),
        )
        return cursor.lastrowid


def update(group_id, name):
    with closing(get_connection()) as conn, conn:
        conn.execute(
            "UPDATE groups SET name = ? WHERE group_id = ?",
            (name, group_id),
        )


def delete(group_id: int):
    with closing(get_connection()) as conn, conn:
        conn.execute("DELETE FROM groups WHERE group_id = ?", (group_id,))

