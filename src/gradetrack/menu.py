import sqlite3

from auth import register
from services import export_service, grade_service, group_service, subject_service, user_service


def export_grades(user):
    try:
        count, directory = export_service.export_grades(user)
        print(f"Выгружено оценок: {count}. Папка: {directory}")
        print("Созданы data.json, data.csv, data.xml, data.yaml")
    except OSError as error:
        print(f"Не удалось записать файлы: {error}")


def read_id(prompt="ID: "):
    try:
        return int(input(prompt))
    except ValueError:
        raise ValueError("Введите целое число") from None


def show_grades(user, group_id=None):
    rows = grade_service.get_display_rows(user, group_id)
    if not rows:
        print("Оценок нет")
        return
    print("ID | Студент | Дисциплина | Оценка | Дата")
    for row in rows:
        print(" | ".join(str(value) for value in row))


def show_groups(user):
    for group in group_service.get_all(user):
        print(f"{group.group_id}. {group.name}")


def show_subjects(user):
    for subject in subject_service.get_all(user):
        print(f"{subject.subject_id}. {subject.name}")


def show_users(user):
    users = user_service.get_all(user)
    groups = {group.group_id: group.name for group in group_service.get_all(user)}
    role_names = {1: "Администратор", 2: "Преподаватель", 3: "Студент"}
    if not users:
        print("Пользователей нет")
    for item in users:
        print(f"{item.user_id}. {item.full_name} | {item.login} | "
              f"{role_names[item.role_id]} | {groups.get(item.group_id, '—')}")


def admin_menu(user):
    while True:
        print("\n===== Администратор =====")
        print("1. Пользователи\n2. Группы\n3. Дисциплины\n0. Выйти из аккаунта")
        choice = input("Выберите действие: ")
        if choice == "1":
            users_menu(user)
        elif choice == "2":
            groups_menu(user)
        elif choice == "3":
            subjects_menu(user)
        elif choice == "0":
            return
        else:
            print("Неверный выбор")


def users_menu(user):
    while True:
        print("\n===== Пользователи =====")
        print("1. Список\n2. Регистрация\n3. Изменить данные\n4. Удалить\n0. Назад")
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                show_users(user)
            elif choice == "2":
                register(user)
            elif choice == "3":
                show_users(user)
                user_id = read_id()
                full_name = input("Новое ФИО: ")
                login_value = input("Новый логин: ")
                show_groups(user)
                group = input("ID группы (пусто для преподавателя/администратора): ")
                user_service.update(user, user_id, full_name, login_value, int(group) if group else None)
                print("Данные изменены")
            elif choice == "4":
                show_users(user)
                user_id = read_id()
                if input("Удалить пользователя и его оценки? (да/нет): ").lower() == "да":
                    user_service.delete(user, user_id)
                    print("Пользователь удалён")
            elif choice == "0":
                return
            else:
                print("Неверный выбор")
        except (ValueError, sqlite3.Error) as error:
            print(f"Ошибка: {error}")


def groups_menu(user):
    while True:
        print("\n===== Группы =====")
        print("1. Список\n2. Добавить\n3. Переименовать\n4. Удалить\n0. Назад")
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                show_groups(user)
            elif choice == "2":
                group_service.create(user, input("Название: "))
                print("Запись добавлена")
            elif choice == "3":
                item_id = read_id()
                group_service.update(user, item_id, input("Новое название: "))
                print("Запись изменена")
            elif choice == "4":
                group_service.delete(user, read_id())
                print("Запись удалена")
            elif choice == "0":
                return
            else:
                print("Неверный выбор")
        except (ValueError, sqlite3.Error) as error:
            print(f"Ошибка: {error}")


def subjects_menu(user):
    while True:
        print("\n===== Дисциплины =====")
        print("1. Список\n2. Добавить\n3. Переименовать\n4. Удалить\n0. Назад")
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                show_subjects(user)
            elif choice == "2":
                subject_service.create(user, input("Название: "))
                print("Запись добавлена")
            elif choice == "3":
                item_id = read_id()
                subject_service.update(user, item_id, input("Новое название: "))
                print("Запись изменена")
            elif choice == "4":
                subject_service.delete(user, read_id())
                print("Запись удалена")
            elif choice == "0":
                return
            else:
                print("Неверный выбор")
        except (ValueError, sqlite3.Error) as error:
            print(f"Ошибка: {error}")


def teacher_menu(user):
    while True:
        print("\n===== Преподаватель =====")
        print("1. Все оценки\n2. Добавить оценку\n3. Изменить оценку\n4. Удалить оценку")
        print("5. Оценки группы\n6. Должники группы\n7. Экспорт всех оценок\n0. Выйти из аккаунта")
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                show_grades(user)
            elif choice == "2":
                show_users(user)
                student_id = read_id("ID студента: ")
                show_subjects(user)
                subject_id = read_id("ID дисциплины: ")
                grade_service.create(user, student_id, subject_id, read_id("Оценка (2–5): "))
                print("Оценка добавлена")
            elif choice == "3":
                grade_id = read_id("ID оценки: ")
                grade_service.update(user, grade_id, read_id("Новая оценка (2–5): "))
                print("Оценка изменена")
            elif choice == "4":
                grade_service.delete(user, read_id("ID оценки: "))
                print("Оценка удалена")
            elif choice == "5":
                show_groups(user)
                show_grades(user, read_id("ID группы: "))
            elif choice == "6":
                show_groups(user)
                debtors = grade_service.get_debtors(user, read_id("ID группы: "))
                print("Студенты с оценкой 2:" if debtors else "Должников нет")
                for student in debtors:
                    print(f"{student.user_id}. {student.full_name}")
            elif choice == "7":
                export_grades(user)
            elif choice == "0":
                return
            else:
                print("Неверный выбор")
        except (ValueError, sqlite3.Error) as error:
            print(f"Ошибка: {error}")


def student_menu(user):
    while True:
        print(f"\n===== Студент: {user.full_name} =====")
        print("1. Мои оценки\n2. Средний балл\n3. Экспорт моих оценок\n0. Выйти из аккаунта")
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                show_grades(user)
            elif choice == "2":
                average = grade_service.get_average(user)
                print(f"Средний балл: {average:.2f}" if average is not None else "Оценок пока нет")
            elif choice == "3":
                export_grades(user)
            elif choice == "0":
                return
            else:
                print("Неверный выбор")
        except (ValueError, sqlite3.Error) as error:
            print(f"Ошибка: {error}")

