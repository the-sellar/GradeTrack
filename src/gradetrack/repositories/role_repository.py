from contextlib import closing

from database.database import get_connection
from models.role import Role


def get_all() -> list[Role]:
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT role_id, name FROM roles ORDER BY role_id").fetchall()
    return [Role(*row) for row in rows]


def get_by_id(role_id: int) -> Role | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT role_id, name FROM roles WHERE role_id = ?", (role_id,)
        ).fetchone()
    return Role(*row) if row else None

