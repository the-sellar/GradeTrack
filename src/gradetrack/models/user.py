from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    full_name: str
    login: str
    password_hash: str
    role_id: int
    group_id: int | None

