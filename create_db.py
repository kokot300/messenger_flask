#!/usr/bin/python

from psycopg2 import connect, errors, OperationalError

USER = 'kokot300'
PASSWORD = ''
HOST = 'localhost'
DATABASE = 'workshop_db'


def lets_create_db():
    try:
        cnx = connect(
            user=USER,
            password=PASSWORD,
            host=HOST
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        c = f'CREATE DATABASE {DATABASE};'
        cursor.execute(c)
        # cursor.commit()
    except OperationalError:
        return 'failed to connect!'
    except errors.DuplicateDatabase:
        return 'db already exists!'
    else:
        cursor.close()
        cnx.close()
        return 'db created!'


def lets_create_table_users():
    try:
        cnx = connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DATABASE
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        c = f'CREATE TABLE users(' \
            f'id serial, ' \
            f'username varchar(255) UNIQUE,' \
            f'hashec_password varchar(80),' \
            f'PRIMARY KEY (id)' \
            f');'
        cursor.execute(c)
        # cursor.commit()
    except OperationalError:
        return 'something went wrong'
    except errors.DuplicateTable:
        return 'table already exists'
    else:
        cursor.close()
        cnx.close()
        return 'all good'


def lets_create_table_mwessages():
    try:
        cnx = connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DATABASE
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        c = f"""CREATE TABLE messages(
                id serial,
                to_id int,
                from_id int,
                PRIMARY KEY (id),
                FOREIGN KEY (to_id) REFERENCES users(id),
                FOREIGN KEY (from_id) REFERENCES users(id)
                );"""
        cursor.execute(c)
        # cursor.commit()
    except OperationalError:
        return 'something went wrong'
    except errors.DuplicateTable:
        return 'table already exists'
    else:
        cursor.close()
        cnx.close()
        return 'all good'


if __name__ == '__main__':
    lets_create_db()
    lets_create_table_users()
    lets_create_table_mwessages()
