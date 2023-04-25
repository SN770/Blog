from models import User, Post, Profile, Repost
from utils import *
import math

class Blog:
    def run(self):
        while True:
            self.menu()

    def menu(self):
        """Стартовое меню блога"""
        print('[1] - Войти')
        print('[2] - Зарегистрироваться')
        print('[3] - Выйти')
        
        user_input = input('Выберите операцию: ')

        if user_input.isdigit():
                user_input = int(user_input)
        else:
            print('Неверный ввод!')
            return

        if user_input == 1:
            self.login()
        elif user_input == 2:
            self.sign_up()
        elif user_input == 3:
            print('Досвидания!')
            exit(0)
        else:
            print('Неверный ввод!')
            return
    
    def login(self):
        """Страница входа"""
        username = input('Введите логин: ')
        password = input('Введите пароль: ')
        
        if User.is_exist(username, password):
            print('Вы вошли!')
            self.user_menu(
                User.get(username=username)
            )
        else:
            print('Неверные данные')
            input()
    
    def sign_up(self):
        """Страница регистрации"""
        username = input('Введите логин: ')
        while not is_valid_username(username):
            username = input('Ошибка! Логин может содержать A-Z, a-z, 0-9, _: ')
        
        password = input('Введите пароль: ')
        is_valid = is_valid_password(password)
        while is_valid != 1:
            if is_valid == -1:
                print('Ошибка! Минимальная длина пароля 8 символов.')
            elif is_valid == 0:
                print('Ошибка! Пароль может содержать A-Z, a-z, 0-9, _')
            password = input('Введите пароль: ')
            is_valid = is_valid_password(password)

        if User.is_exist(username):
            print('Ошибка! Пользователь с таким логином уже существует!')
        else:
            print('Вы были зарегистрированы!')
            pid = Profile.create(
                **{
                    'name' : 'Не заполнено',
                    'surname' : 'Не заполнено',
                    'email' : 'Не заполнено',
                    'age' : 'Не заполнено',
                }
            )
            User.create(
                **{
                    'profile_id' : pid, 
                    'username' : username, 
                    'password' : password
                }
            )

    def user_menu(self, user):
        """Страница меню пользователя (авторизованного)"""
        user_input = input('[1] - Перейти в профиль\n[2] - Создать пост\n[3] - Посмотреть посты\n[4] - Выйти\nВыберите операцию: ')
    
        while user_input not in '1234' or len(user_input) != 1:
            user_input = input('[1] - Перейти в профиль\n[2] - Создать пост\n[3] - Посмотреть посты\n[4] - Выйти\nВыберите опeрацию: ')

        if user_input == '1':
            self.profile_page(user) 
            self.user_menu(user)
        elif user_input == '2':
            self.create_post(user)       
            self.user_menu(user)
        elif user_input == '3':
            self.posts_page(user)
            self.user_menu(user)
        else:
            return
        
    def profile_page(self, user):
        """Страница профиля пользователя"""
        profile = Profile.get(user.profile_id)
        print(f'\nИмя: \t{profile.name}\nФамилия:{profile.surname}\nEmail:\t{profile.email}\nAge:\t{profile.age}')
        print("[1] - Редактировать имя\n[2] - Редактировать фамилию\n[3] - Редактировать email\n[4] - Редактировать возраст\n[5] - Мои посты\n[6] - Моя стена\n[7] - Главное меню\nВведите операцию: ", end='')

        user_input = input()
        
        while user_input not in '1234567' or len(user_input) > 1:
            user_input = input('Неверный ввод!\nВведите операцию: ')
        
        if user_input == '7':
            return
        
        if user_input == '1':
            new_name = input('Введите новое имя: ')
            while not is_valid_name(new_name):
                new_name = input('Ошибка! Имя может содержать A-Z, a-z: ')
            profile.name = new_name
            Profile.update(profile.id, **{'name' : new_name})
            print('Ваше имя было изменено!')
            self.profile_page(user)
        elif user_input == '2':
            new_surname = input('Введите новую фамилию: ')
            while not is_valid_name(new_surname):
                new_surname = input('Ошибка! Фамилия может содержать A-Z, a-z: ')
            Profile.update(profile.id, **{'surname' : new_surname})
            print('Ваша фамилия была изменена!')
            self.profile_page(user)        
        elif user_input == '3':
            new_email = input('Введите новый email: ')
            while not is_valid_email(new_email):
                new_email = input('Ошибка! Неверный адрес email: ')
            Profile.update(profile.id, **{'email' : new_email})
            print('Email был изменен!')
            self.profile_page(user)
        elif user_input == '4':
            new_age = input('Введите новый возраст: ')
            while True:
                try:
                    new_age = int(new_age)
                    break
                except ValueError:
                    new_age = input('Ошибка! Ожидалось число: ')
            Profile.update(profile.id, **{'age' : new_age})
            print('Возраст был изменен!')
            self.profile_page(user)
        elif user_input == '5':
            self.user_posts_page(user)
            self.profile_page(user)
        elif user_input == '6':
            self.user_reposts_page(user)
            self.profile_page(user)
        
    def user_reposts_page (self, user):
        """Стена пользователя"""
        posts = Post.get_user_posts(user.id)
        limit = 5
        num = len(posts)

        total_pages = math.ceil(num / limit)
        current_page = 1
        
        while True:
            start = (current_page - 1) * limit
            end = (start + 5) if num - start >= 5 else (num - start) % 5 + start
            cpi = list()

            for post in posts[start:end]:
                print('[id: ' + str(post['id']) + '] ' + post['title'])
                print(post['text'])
                cpi.append(post['id'])
                print()
            
            av_opt = ['3', '4', '5']

            if current_page < total_pages:
                av_opt.append('1')
                print('[1] - Следующая страница')
            if current_page > 1:
                av_opt.append('2')
                print('[2] - Предыдущая страница')
            
            print('[3] - Посмотреть пост')            
            print('[4] - Удалить пост')            
            print('[5] - Назад')           
            
            user_input = input('Введите опцию: ')
        
            while user_input not in av_opt:
                user_input = input('Ошибка! Введите опцию: ')
            
            if user_input == '1':
                current_page += 1
            elif user_input == '2':
                current_page -= 1
            elif user_input == '3':
                post_id = input('Введите id поста: ')
                while not post_id.isdigit() or int(post_id) not in cpi:
                    post_id = input('Неверный ввод! Введите id поста: ')
                for post in posts:
                    if post['id'] == int(post_id):
                        self.post_page(post, 'reviewer')
            elif user_input == '4':
                post_id = input('Введите id поста: ')
                while not post_id.isdigit() or int(post_id) not in cpi:
                    post_id = input('Неверный ввод! Введите id поста: ')
                Repost.delete(user.id, post_id)
                
                posts = Post.get_user_posts(user.id)

                print('Пост был удалён!')
                input()
            else:
                break

    def create_post(self, user):
        """Страница создания поста"""
        post_name = input('Введите название поста: ')
        print("Введите текст, для завершения введите ':q':")
        post_text = ''

        while True:
            row = input()
            if ':q' in row:
                row = row.replace(':q', '')
                post_text += row + r'\n'
                break
            else:
                post_text += row + r'\n'

        data = {
            'user_id' : user.id, 
            'title'   : post_name, 
            'text'    : post_text
        }

        if Post.create(**data):
            print('Пост был создан!')
        else:
            print('Ошибка, обратитесь к админу!')
        

    def posts_page(self, user):
        """Страница всех постов"""
        posts = Post.get_all()
        limit = 5
        num = len(posts)

        total_pages = math.ceil(num / limit)
        current_page = 1
        
        while True:
            start = (current_page - 1) * limit
            end = (start + 5) if num - start >= 5 else (num - start) % 5 + start
            cpi = list()

            for post in posts[start:end]:
                print('[id: ' + str(post['id']) + '] ' + post['title'])
                print(post['text'])
                cpi.append(post['id'])
                print()
            
            av_opt = ['3', '4', '5']

            if current_page < total_pages:
                av_opt.append('1')
                print('[1] - Следующая страница')
            if current_page > 1:
                av_opt.append('2')
                print('[2] - Предыдущая страница')
            
            print('[3] - Посмотреть пост')            
            print('[4] - Репостнуть')            
            print('[5] - Назад')           
            
            user_input = input('Введите опцию: ')
        
            while user_input not in av_opt:
                user_input = input('Ошибка! Введите опцию: ')
            
            if user_input == '1':
                current_page += 1
            elif user_input == '2':
                current_page -= 1
            elif user_input == '3':
                post_id = input('Введите id поста: ')

                while not post_id.isdigit() or int(post_id) not in cpi:
                    post_id = input('Неверный ввод! Введите id поста: ')
                
                for post in posts:
                    if post['id'] == int(post_id):
                        self.post_page(post, 'reviewer')
            elif user_input == '4':
                post_id = input('Введите id поста: ')

                while not post_id.isdigit() or int(post_id) not in cpi:
                    post_id = input('Неверный ввод! Введите id поста: ')

                if User.is_creator(user.id, post_id):
                    print('Нельзя репостить свои записи!')
                    input()
                    print()
                else:
                    if Repost.create(user_id = user.id, post_id = post_id):
                        input('Вы репостнули пост!\n')
                    else:
                        print('Что - то пошло не так, обратитесь к администратору!')
                    
            else:
                break

    def user_posts_page (self, user):
        """Страница записей пользователя"""
        posts = User.get_posts(user.id)
        limit = 5
        num = len(posts)
        total_pages = math.ceil(num / limit)
        current_page = 1
        
        while True:
            start = (current_page - 1) * limit
            end = (start + 5) if num - start >= 5 else (num - start) % 5 + start
            cpi = list()

            for post in posts[start:end]:
                print('[id: ' + str(post['id']) + '] ' + post['title'])
                cpi.append(post['id'])
                print(post['text'])
                print()
            
            av_opt = ['3', '4']

            if current_page < total_pages:
                av_opt.append('1')
                print('[1] - Следующая страница')
            if current_page > 1:
                av_opt.append('2')
                print('[2] - Предыдущая страница')
            
            print('[3] - Редактировать пост')            
            print('[4] - Назад')           
            
            user_input = input('Введите опцию: ')
        
            while user_input not in av_opt:
                user_input = input('Ошибка! Введите опцию: ')
            
            if user_input == '1':
                current_page += 1
            elif user_input == '2':
                current_page -= 1
            elif user_input == '3':
                post_id = input('Введите id поста: ')

                while not post_id.isdigit() or int(post_id) not in cpi:
                    post_id = input('Неверный ввод! Введите id поста: ')
                
                for post in posts:
                    if post['id'] == int(post_id):
                        self.post_page(post, 'creator')
            else:
                break
        

    def post_page(self, post, rights = 'reviewer'):
        """
        Просмотреть / Редактировать пост
        :param post: - dict
        :param rights: - str, 'reviewer', 'creator'
        """
        if rights == 'creator':
            user_input = input('Название: \t{}\nТекст:\n{}\n[1] - Изменить название\n[2] - Изменить текст\n[3] - Удалить пост\n[4] - назад\nВведите операцию: '.format(post['title'], post['text']))

            while len(user_input) != 1 or user_input not in '1234':
                user_input = 'Неверный ввод! Введите операцию: '
            
            if user_input == '1':
                new_title = input('Введите новое название: ')
                post['title'] = new_title
                Post.update(
                    post['id'], 
                    **{
                        'title' : post['title']
                    }
                )
                print('Название обновлено!')
            elif user_input == '2':
                print("Введите текст, для завершения введите ':q':")
                new_text = ''
                while True:
                    row = input()
                    if ':q' in row:
                        row = row.replace(':q', '')
                        new_text += row + '\n'
                        break
                    else:
                        new_text += row + '\n'
                
                post['text'] = new_text

                Post.update(
                    post['id'], 
                    **{
                        'text' : post['text']
                    }
                )
                print('Текст обновлен!')
            elif user_input == '3':
                Post.delete(post['id'])
                print('Пост был удалён!\n')
                input()
                return
            else:
                return
        else:
            user_input = input('Название: \t{}\nТекст:\n{}\n[3] - Назад\nВведите операцию: '.format(post['title'], post['text']))

            while len(user_input) != 1 or user_input != '3':
                user_input = input('Неверный ввод! Введите операцию: ')

            if user_input == '3':
                return    
