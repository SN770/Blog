from utils import is_valid_name, is_valid_password, is_valid_username, is_exist, is_valid_email
from models import Profile, User, Post
from blog import Blog
# Главное меню
# Здравствуйте!
# [1] - Войти 
# [2] - Зарегестрироваться
# [3] - Выйти
#   1 - Меню входа:
#       Введите логин: ...              
#       Введите пароль: ...             
#           -- [1] - Перейти в профиль  
#               -- Name: name (если None, вывести Не заполнено)
#               -- Surname: surname
#               -- Age: age
#               -- Email: email
#                   -- [1] - Редактировать имя
#                       -- Введите новое имя: (Проверяем)
#                           -- Имя изменено! ...
#                           -- Некорректное имя! 
#                   -- [2] - Редактировать фамилию
#                   -- [3] - Редактировать возраст
#                   -- [4] - Редактировать email
#                   -- [5] - Назад
#           -- [2] - Создать пост
#           -- [3] - Лента (постов)
#           -- [4] - Выйти
#           -- Данные неверные 
#  2 - Меню регистрации: 
#       Введите логин: ...              -- проверка на верность (только английские буквы, цифры, _, не может начинаться с цифры)
#           -- Логин занят!
#       Введите пароль: ...             -- проверка на верность (только английские буквы, цифры, _, мин длина 8)
#       Регистрация завершена успешно! -> Главное меню
# class User:
#       -- username
#       -- password
#       -- Profile
# функции для проверки username, password, name
#    is_correct_name
#    is_correct_username
#    is_correct_password
# class Profile:
#       -- name
#       -- age
#       -- email
#       -- surname

# class Post:
#       -- user_id (int)
#       -- title (str)
#       -- content (str)

def create_post(user):
    title = input('Введите название поста: ')
    content = input('Введите текст поста: ')

    while len(title) == 0 or len(content) == 0:
        print('Название или содержание не могут быть пустыми!')
        title = input('Введите название поста: ')
        content = input('Введите текст поста: ')

    post = Post(user.id, title, content)
    posts.append(post)

    print('Пост был создан!')
    input()
    user_menu(user)

def profile_info(user):
    for i in users:
        print(i.id, i.username, i.password)

    print('Посты:')
    for post in posts:
        if post.user_id == user.id:
            print(post.user_id, post.title, post.content)
    print()
    print('\nИмя:', user.profile.name if user.profile.name is not None else 'не заполнено')
    print('Фамилия:', user.profile.surname if user.profile.surname is not None else 'не заполнено')
    print('Email:', user.profile.email if user.profile.email is not None else 'не заполнено')
    print('Возраст:', user.profile.age if user.profile.age is not None else 'не заполнено')

    question = """
[1] - Редактировать имя
[2] - Редактировать фамилию
[3] - Редактировать email
[4] - Редактировать возраст
[5] - Главное меню
Введите операцию:"""

    user_input = input(question)

    while user_input not in '12345' or len(user_input) != 1:
        user_input = input("Неверный ввод!" + question)
    
    if user_input == '1':
        new_name = input('Введите новое имя: ')
        while not is_valid_name(new_name):
            new_name = input('Ошибка! Имя может содержать A-Z, a-z: ')
        user.profile.name = new_name
        print('Имя было изменено!')
        profile_info(user)
    elif user_input == '2':
        new_surname = input('Введите новую фамилию: ')
        while not is_valid_name(new_surname):
            new_surname = input('Ошибка! Фамилия может содержать A-Z, a-z: ')
        user.profile.surname = new_surname
        print('Фамилия была изменена!')
        profile_info(user)
    elif user_input == '3':
        new_email = input('Введите новый email: ')
        while not is_valid_email(new_email):
            new_email = input('Ошибка! Неверный адрес email: ')
        user.profile.email = new_email
        print('Email был изменен!')
        profile_info(user)
    elif user_input == '4':
        new_age = input('Введите новый возраст: ')
        while True:
            try:
                new_age = int(new_age)
                break
            except ValueError:
                new_age = input('Ошибка! Ожидалось число: ')
        user.profile.age = new_age
        print('Возраст был изменен!')
        profile_info(user)
    else:
        user_menu(user)

def user_menu(user):
    user_input = input('[1] - Перейти в профиль\n[2] - Создать пост\n[3] - Выйти\nВыберите опрацию: ')
    
    while user_input not in '123' or len(user_input) != 1:
        user_input = input('Неверный ввод!\n[1] - Перейти в профиль\n[2] - Создать пост\n[3] - Выйти\nВыберите опрацию: ')

    if user_input == '1':
        profile_info(user) 
    elif user_input == '2':
        create_post(user)       
    else:
        return
        
def login():
    global users
    username = input('Введите логин: ')
    password = input('Введите пароль: ')
    
    is_logged = False

    for user in users:
        if user.username == username and user.password == password:
            print('Вы вошли!')
            input()
            is_logged = True
            break
    
    if not is_logged:
        print('Данные неверные.')
        input()
    else:
        user_menu(user)

def sign_up():
    global users
    username = input('Введите логин: ')
    password = input('Введите пароль: ')
    
    while not is_valid_username(username):
        username = input('Ошибка! Логин может содержать A-Z, a-z, 0-9, _: ')

    is_valid = is_valid_password(password)

    while not (is_valid == 1):
        if is_valid == -1:
            print('Ошибка! Минимальная длина пароля 8 символов.')
        elif is_valid == 0:
            print('Ошибка! Пароль может содержать A-Z, a-z, 0-9, _')
        password = input('Введите пароль: ')
        is_valid = is_valid_password(password)
    
    if is_exist(users, username):
        print('Ошибка! Пользователь с таким логином уже существует!')
    else:
        print('Вы были зарегестрированы!')
        user = User(users[-1].id + 1, username, password, Profile())
        users.append(user)
    
if __name__ == '__main__':
    blog = Blog()
    blog.run()