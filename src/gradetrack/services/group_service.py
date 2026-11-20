from repositories import group_repository, user_repository
from services.auth_service import ADMIN, TEACHER, STUDENT, require_role


def get_all(user):
    require_role(user, ADMIN, TEACHER, STUDENT)
    return group_repository.get_all()


def validate_name(name, group_id=None):
    if not name.strip():
        raise ValueError("Название не может быть пустым")
    for item in group_repository.get_all():
        if item.name.casefold() == name.strip().casefold() and item.group_id != group_id:
            raise ValueError("Такое название уже существует")


def create(user, name):
    require_role(user, ADMIN)
    validate_name(name)
    return group_repository.create(name.strip())


def update(user, group_id, name):
    require_role(user, ADMIN)
    if not group_repository.get_by_id(group_id):
        raise ValueError("Группа не найдена")
    validate_name(name, group_id)
    group_repository.update(group_id, name.strip())


def delete(user, group_id):
    require_role(user, ADMIN)
    if not group_repository.get_by_id(group_id):
        raise ValueError("Группа не найдена")
    if any(item.group_id == group_id for item in user_repository.get_all()):
        raise ValueError("Нельзя удалить группу, в которой есть студенты")
    group_repository.delete(group_id)

