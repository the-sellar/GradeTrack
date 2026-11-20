from contextlib import closing

from database.database import get_connection
from models.user import User


def get_all() -> list[User]:
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT user_id, full_name, login, password_hash, role_id, group_id FROM users ORDER BY user_id").fetchall()
    return [User(*row) for row in rows]


def get_by_id(user_id: int) -> User | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT user_id, full_name, login, password_hash, role_id, group_id FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    return User(*row) if row else None


def create(full_name, login, password_hash, role_id, group_id):
    with closing(get_connection()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO users (full_name, login, password_hash, role_id, group_id) VALUES (?, ?, ?, ?, ?)",
            (full_name, login, password_hash, role_id, group_id,),
        )
        return cursor.lastrowid


def update(user_id, full_name, login, password_hash, role_id, group_id):
    with closing(get_connection()) as conn, conn:
        conn.execute(
            "UPDATE users SET full_name = ?, login = ?, password_hash = ?, role_id = ?, group_id = ? WHERE user_id = ?",
            (full_name, login, password_hash, role_id, group_id, user_id),
        )


def delete(user_id: int):
    with closing(get_connection()) as conn, conn:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))


def get_by_login(login: str) -> User | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT user_id, full_name, login, password_hash, role_id, group_id FROM users WHERE login = ?", (login,)
        ).fetchone()
    return User(*row) if row else None

