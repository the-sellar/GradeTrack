from services import auth_service, group_service, user_service


def login():
    login_value = input("Логин: ")
    password = input("Пароль: ")
    user = auth_service.authenticate(login_value, password)
    if not user:
        print("Неверный логин или пароль")
    return user


def register(user):
    full_name = input("ФИО: ")
    login_value = input("Логин: ")
    password = input("Пароль: ")
    for role in user_service.get_roles(user):
        print(f"{role.role_id}. {role.name}")
    role_id = int(input("ID роли: "))
    group_id = None
    if role_id == auth_service.STUDENT:
        for group in group_service.get_all(user):
            print(f"{group.group_id}. {group.name}")
        group_id = int(input("ID группы: "))
    user_service.register(user, full_name, login_value, password, role_id, group_id)
    print("Пользователь зарегистрирован")
