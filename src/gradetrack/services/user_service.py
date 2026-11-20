from repositories import group_repository, role_repository, user_repository
from services.auth_service import ADMIN, TEACHER, STUDENT, hash_password, require_role


def get_all(user):
    require_role(user, ADMIN, TEACHER)
    users = user_repository.get_all()
    if user.role_id == TEACHER:
        return [item for item in users if item.role_id == STUDENT]
    return users


def get_roles(user):
    require_role(user, ADMIN)
    return role_repository.get_all()


def validate(full_name, login, role_id, group_id, user_id=None):
    if not full_name.strip() or not login.strip():
        raise ValueError("ФИО и логин не могут быть пустыми")
    existing = user_repository.get_by_login(login.strip())
    if existing and existing.user_id != user_id:
        raise ValueError("Такой логин уже занят")
    if not role_repository.get_by_id(role_id):
        raise ValueError("Роль не найдена")
    if role_id == STUDENT:
        if not group_repository.get_by_id(group_id):
            raise ValueError("Для студента нужно выбрать существующую группу")
    elif group_id is not None:
        raise ValueError("Группа указывается только для студента")


def register(user, full_name, login, password, role_id, group_id):
    require_role(user, ADMIN)
    validate(full_name, login, role_id, group_id)
    if not password.strip():
        raise ValueError("Пароль не может быть пустым")
    return user_repository.create(
        full_name.strip(), login.strip(), hash_password(password), role_id, group_id
    )


def update(user, user_id, full_name, login, group_id):
    require_role(user, ADMIN)
    target = user_repository.get_by_id(user_id)
    if not target:
        raise ValueError("Пользователь не найден")
    validate(full_name, login, target.role_id, group_id, user_id)
    user_repository.update(
        user_id, full_name.strip(), login.strip(), target.password_hash, target.role_id, group_id
    )


def delete(user, user_id):
    require_role(user, ADMIN)
    target = user_repository.get_by_id(user_id)
    if not target:
        raise ValueError("Пользователь не найден")
    if target.role_id == ADMIN:
        raise ValueError("Удаление администратора недоступно")
    user_repository.delete(user_id)
