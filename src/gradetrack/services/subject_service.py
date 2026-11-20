from repositories import subject_repository, grade_repository
from services.auth_service import ADMIN, TEACHER, STUDENT, require_role


def get_all(user):
    require_role(user, ADMIN, TEACHER, STUDENT)
    return subject_repository.get_all()


def validate_name(name, subject_id=None):
    if not name.strip():
        raise ValueError("Название не может быть пустым")
    for item in subject_repository.get_all():
        if item.name.casefold() == name.strip().casefold() and item.subject_id != subject_id:
            raise ValueError("Такое название уже существует")


def create(user, name):
    require_role(user, ADMIN)
    validate_name(name)
    return subject_repository.create(name.strip())


def update(user, subject_id, name):
    require_role(user, ADMIN)
    if not subject_repository.get_by_id(subject_id):
        raise ValueError("Дисциплина не найдена")
    validate_name(name, subject_id)
    subject_repository.update(subject_id, name.strip())


def delete(user, subject_id):
    require_role(user, ADMIN)
    if not subject_repository.get_by_id(subject_id):
        raise ValueError("Дисциплина не найдена")
    if any(item.subject_id == subject_id for item in grade_repository.get_all()):
        raise ValueError("Нельзя удалить дисциплину, по которой есть оценки")
    subject_repository.delete(subject_id)

