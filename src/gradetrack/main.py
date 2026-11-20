import sqlite3

from auth import login
from database.database import create_database
from menu import admin_menu, teacher_menu, student_menu
from services.auth_service import ADMIN, TEACHER, STUDENT


def main():
    create_database()
    while True:
        print("\n===== GradeTrack =====\n1. Вход\n0. Выход")
        choice = input("Выберите действие: ")
        if choice == "0":
            print("До свидания!")
            break
        if choice != "1":
            print("Неверный выбор")
            continue
        user = login()
        if not user:
            continue
        if user.role_id == ADMIN:
            admin_menu(user)
        elif user.role_id == TEACHER:
            teacher_menu(user)
        elif user.role_id == STUDENT:
            student_menu(user)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nРабота завершена")
    except sqlite3.Error as error:
        print(f"Ошибка базы данных: {error}")
