import hashlib
import hmac
import secrets

from repositories import user_repository

ADMIN = 1
TEACHER = 2
STUDENT = 3


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
    return f"{salt}${digest}"


def authenticate(login: str, password: str):
    user = user_repository.get_by_login(login.strip())
    if not user:
        return None
    salt, expected = user.password_hash.split("$", 1)
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()
    return user if hmac.compare_digest(actual, expected) else None


def require_role(user, *roles):
    if user is None or user.role_id not in roles:
        raise ValueError("Недостаточно прав для этого действия")
