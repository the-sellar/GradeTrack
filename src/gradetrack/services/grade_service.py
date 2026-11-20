from datetime import date

from repositories import grade_repository, group_repository, subject_repository, user_repository
from services.auth_service import TEACHER, STUDENT, require_role


def validate(student_id, subject_id, value):
    student = user_repository.get_by_id(student_id)
    if not student or student.role_id != STUDENT:
        raise ValueError("Студент не найден")
    if not subject_repository.get_by_id(subject_id):
        raise ValueError("Дисциплина не найдена")
    if type(value) is not int or not 2 <= value <= 5:
        raise ValueError("Оценка должна быть целым числом от 2 до 5")


def create(user, student_id, subject_id, value):
    require_role(user, TEACHER)
    validate(student_id, subject_id, value)
    return grade_repository.create(student_id, subject_id, value, date.today().isoformat())


def update(user, grade_id, value):
    require_role(user, TEACHER)
    grade = grade_repository.get_by_id(grade_id)
    if not grade:
        raise ValueError("Оценка не найдена")
    validate(grade.student_id, grade.subject_id, value)
    grade_repository.update(grade_id, grade.student_id, grade.subject_id, value, grade.grade_date)


def delete(user, grade_id):
    require_role(user, TEACHER)
    if not grade_repository.get_by_id(grade_id):
        raise ValueError("Оценка не найдена")
    grade_repository.delete(grade_id)


def get_grades(user, group_id=None):
    require_role(user, TEACHER, STUDENT)
    grades = grade_repository.get_all()
    if user.role_id == STUDENT:
        return [grade for grade in grades if grade.student_id == user.user_id]
    if group_id is not None:
        if not group_repository.get_by_id(group_id):
            raise ValueError("Группа не найдена")
        students = {item.user_id for item in user_repository.get_all() if item.group_id == group_id}
        grades = [grade for grade in grades if grade.student_id in students]
    return grades


def get_display_rows(user, group_id=None):
    grades = get_grades(user, group_id)
    users = {item.user_id: item.full_name for item in user_repository.get_all()}
    subjects = {item.subject_id: item.name for item in subject_repository.get_all()}
    return [
        (grade.grade_id, users[grade.student_id], subjects[grade.subject_id], grade.value, grade.grade_date)
        for grade in grades
    ]


def get_average(user):
    require_role(user, STUDENT)
    grades = get_grades(user)
    return sum(grade.value for grade in grades) / len(grades) if grades else None


def get_debtors(user, group_id):
    require_role(user, TEACHER)
    grades = get_grades(user, group_id)
    student_ids = {grade.student_id for grade in grades if grade.value == 2}
    return [item for item in user_repository.get_all() if item.user_id in student_ids]
