from database.database import DB_FILE, create_database, print_tables


def main():
    print("Hello, World! GradeTrack - система учёта оценок студентов.")

    create_database()
    print(f"База данных создана: {DB_FILE}")
    print_tables()


if __name__ == "__main__":
    main()
