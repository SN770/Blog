import pymysql
from pymysql.cursors import DictCursor

class DBService:
    def __init__ (self):
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',      
            db = 'blog',
            charset = 'utf8mb4',
            cursorclass = DictCursor
        )
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def select(self, table_name, columns = '*', where = '1', query = None):
        """
        :param table_name: - str, имя таблицы
        :param columns: - list, столбцы для выборки
        :param where: - str, условие выборки
        :param query: - str, запрос для выборки
        :return cursor: - результат запроса
        """

        if query is None:
            if columns != '*':
                cols = ''
                for i in columns:
                    cols += i + ','
                columns = cols[:-1]
            query = "SELECT {} FROM {} WHERE {}".format(columns, table_name, where)

        self.execute(query)
        return self.cursor
    
    def insert(self, table_name, data):
        """
        :param table_name:  - имя таблицы
        :param data:        - данные для вставки (dict)
        """
        keys = ','.join(data.keys())
        values = ','.join(["'"+el+"'" if isinstance(el, str) else str(el) for el in data.values()])
        query = "INSERT INTO {} ({}) VALUES ({})".format(table_name, keys, values)
        self.execute(query)

    def update(self, table_name, data, where):
        """
        :param table_name: - str, имя таблицы
        :param data: - dict, данные для изменения
        :param where: - str, условие обновления
        """
        set_ = ','.join([i + '=' + ("'" + data[i] + "'" if isinstance(data[i], str) else str(data[i])) for i in data])
        query = 'UPDATE {} SET {} WHERE {}'.format(table_name, set_,where)
        self.execute(query)

    def delete(self, table_name, where):
        """
        :param table_name: - str, имя таблицы
        :param where: - str, условие удаление
        """
        query = 'DELETE FROM {} WHERE {}'.format(table_name, where)
        self.execute(query)

    def __exit__ (self):
        self.cursor.close()
        self.connection.close()
