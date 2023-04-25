from DBService import *

class Profile:
    def __init__(self, id, name, surname, email, age):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.age = age
    
    @classmethod
    def get(cls, id):
        """
        :param id: - int
        :return Profile: - class Profile
        :return None: - профиль отсутствует
        """
        db = DBService()
        data = db.select(
            'profile',
            where='id = {}'.format(id)
        ).fetchone()

        if data is None: 
            return None
        else:
            return cls(**data)

    @classmethod
    def update(cls, id, **data):
        """
        :param id: - int
        :param data: - kwargs
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.update(
                'profile',
                data,
                'id = {}'.format(id)
            )
            return True
        except Exception as e:
            print(e)
            return False
    
    @classmethod
    def create(cls, **kwargs):
        """
        :param kwargs: - name, surname, email, age
        :return int: - успех, айди вставленного значения
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.insert(
                'profile',
                kwargs
            )
            pid = db.select(None, 
                query = 'select max(id) from profile'
            )
            return int(pid.fetchone()['max(id)'])
        except Exception as e:
            print(e)
            return False


    @classmethod
    def delete(cls, id):
        """
        :param id: - int
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.delete(
                'profile',
                'id = {}'.format(id)
            )
            return True
        except Exception as e:
            print(e)
            return False

class User:
    def __init__(self, id, profile_id, username, password):
        self.id = id
        self.profile_id = profile_id
        self.username = username
        self.password = password

    @classmethod
    def get(cls, id = None, username = None):
        """
        :param id: - int, выбока по id
        :param username: - str, выборка по логину
        :return User: - class User
        :return None: - пользователь отсутствует
        """
        db = DBService()
        if id is not None:
            data = db.select(
                'user',
                where='id = {}'.format(id)
            ).fetchone()
        else:
            data = db.select(
                'user',
                where='username = \'{}\''.format(username)
            ).fetchone()
            
        if data is None: 
            return None
        else:
            return cls(**data)

    @classmethod
    def get_posts(cls, user_id):
        """
        :param user_id: - int
        :return list: - список записей пользователя (Post)
        :return None: - записи отсутствуют
        """

        db = DBService()
        res = db.select(
            'post',
            where = f'user_id = {user_id}'
        )

        return res.fetchall()

    @classmethod
    def is_creator(cls, user_id, post_id):
        """
        :param user_id: - int
        :param post_id: - int
        :return True: - если создатель
        :return False:
        """
        db = DBService()
        res = db.select(
            'post',
            query = 'SELECT user_id FROM post WHERE id = {post_id}'.format(post_id = post_id)
        )
        return res.fetchone()['user_id'] == user_id

    @classmethod
    def update(cls, id, **data):
        """
        :param id: - int
        :param data: - kwargs
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.update(
                'user',
                data,
                'id = {}'.format(id)
            )
            return True
        except Exception as e:
            print(e)
            return False
    
    @classmethod
    def create(cls, **kwargs):
        """
        :param kwargs: - profile_id, username, password
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.insert(
                'user',
                kwargs
            )
            return True
        except Exception as e:
            print(e)
            return False


    @classmethod
    def delete(cls, id):
        """
        :param id: - int
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.delete(
                'user',
                'id = {}'.format(id)
            )
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def is_exist(cls, username, password=None):
        """
        :param username: - str
        :param password: - None or str
        :return True: - существует
        :return False: - не существует
        """
        try:
            db = DBService()
            if password is not None:
                result = db.select(
                    'user', 
                    where = f"username = '{username}' AND password = '{password}'"
                )
                return result.rowcount == 1
            else:
                result = db.select(
                    'user', 
                    where = f"username = '{username}'"
                )
                return result.rowcount >= 1
        except Exception as e:
            print(e)
            return False

class Post:
    def __init__(self, id, user_id, title, text):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.text = text

    @classmethod
    def get(cls, id):
        """
        :param id: - int
        :return Post: - class Post
        :return None: - запись отсутствует
        """
        db = DBService()
        data = db.select(
            'post',
            where='id = {}'.format(id)
        ).fetchone()

        if data is None: 
            return None
        else:
            return cls(**data)

    @classmethod
    def get_all(cls):
        """
        :return list: - список записей (Post)
        :return None: - записи отсутствуют
        """
        db = DBService()
        res = db.select('post')

        return res.fetchall()

    @classmethod
    def get_user_posts(cls, user_id):
        """
        :param user_id: - int
        :return list: - список записей (Post)
        :return None: - записи отсутствуют
        """
        db = DBService()
        res = db.select(
            'repost', 
            query = f'SELECT post.* FROM repost INNER JOIN post ON post.id = repost.post_id WHERE repost.user_id = { user_id }'
        )

        return res.fetchall()

    @classmethod
    def update(cls, id, **data):
        """
        :param id: - int
        :param data: - kwargs
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.update(
                'post',
                data,
                'id = {}'.format(id)
            )
            return True
        except Exception as e:
            print(e)
            return False
    
    @classmethod
    def create(cls, **kwargs):
        """
        :param kwargs: - user_id, title, text
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.insert(
                'post',
                kwargs
            )
            return True
        except Exception as e:
            print(e)
            return False


    @classmethod
    def delete(cls, id):
        """
        :param id: - int
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.delete(
                'post',
                'id = {}'.format(id)
            )
            return True
        except Exception as e:
            print(e)
            return False
        
class Repost:
    @classmethod
    def create(cls, **kwargs):
        """
        :param kwargs: - user_id, post_id
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.insert(
                'repost',
                kwargs
            )
            return True
        except Exception as e:
            print(e)
            return False


    @classmethod
    def delete(cls, user_id, post_id):
        """
        :param user_id: - int
        :param post_id: - int
        :return True: - успех
        :return False: - ошибка
        """
        try:
            db = DBService()
            db.delete(
                'repost',
                f'user_id = { user_id } AND post_id = { post_id }'
            )
            return True
        except Exception as e:
            print(e)
            return False 