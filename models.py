#!/usr/bin/python

from psycopg2 import connect, OperationalError, errors
from clcrypto import hash_password, check_password


# class Cursor:
#     def __init__(self, user='kokot300', password='', host='localhost', database='workshop_db'):
#         self.user = user
#         self.password = password
#         self.host = host
#         self.database = database
#
#     def cursor(self):
#         try:
#             cnx = connect(
#                 user=self.user,
#                 password=self.password,
#                 host=self.host,
#                 database=self.database
#
#             )
#             cnx.autocommit = True
#             cursor = cnx.cursor()
#             return cursor
#         except OperationalError as e:
#             return f'{e}'
#         except errors.DuplicateDatabase as e:
#             return f'{e}'
#         except errors.DuplicateTable as e:
#             return f'{e}'


class User:
    def __init__(self, username="", password="", salt=None):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def safe_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id;"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s;"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_name(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
        cursor.execute(sql, (username,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            print('models ', loaded_user)
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

    def __str__(self):
        return f'id {self._id}, user {self.username}, pass {self._hashed_password}'


class Messages:
    def __init__(self, from_id='', to_id='', text=''):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_data = None

    @property
    def id(self):
        return self._id

    @property
    def time_then(self):
        try:
            cnx = connect(
                user='kokot300',
                password='',
                host='localhost',
                database='workshop_db'

            )
            cnx.autocommit = True
            cursor = cnx.cursor()
            c = f'SELECT time_then FROM messages WHERE id={self.id}'
            cursor.execute(c)
        except OperationalError as e:
            return f'{e}'
        print(cursor.fetchone())
        return cursor.fetchone()

    def safe_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, content)
                            VALUES(%s, %s, %s) RETURNING id"""
            values = (int(self.from_id), int(self.to_id), self.text)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE messages SET from_id = %s, to_id = %s, content=%s
                           WHERE id=%s"""
            values = (self.form_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, from_id):
        sql = "SELECT id, from_id, to_id, content, time_then FROM messages WHERE from_id=%s;"
        message = []
        cursor.execute(sql, (from_id,))
        for row in cursor.fetchall():
            id_, from_id, to_id, content, time_then = row
            loaded_message = Messages()
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.text = content
            loaded_message.creation_data = time_then
            message.append(loaded_message)
        return message

    def __str__(self):
        return f'message from {self.from_id} to {self.to_id} sent at {self.creation_data} says:\n {self.text}'
