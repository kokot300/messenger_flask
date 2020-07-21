#!/usr/bin/python

from argparse import ArgumentParser
import models as m
import clcrypto as cl
from psycopg2 import connect

parser = ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_password", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action='count')
parser.add_argument("-d", "--delete", help="delete user", action='count')
parser.add_argument("-e", "--edit", help="edit user", action='count')

args = parser.parse_args()

print(args)


def conn():
    cnx = connect(
        user='kokot300',
        password='',
        host='localhost',
        database='workshop_db'
    )
    cnx.autocommit = True
    cursor = cnx.cursor()
    return cursor


cursor = conn()


def create_user(username, password):
    # hashed_pass = cl.hash_password(args.password)
    # print()
    if len(password) < 8:
        print('password too short!')
        return
    user = m.User(username, password)
    msg = user.load_user_by_name(cursor, username)
    if msg is None:
        user.safe_to_db(cursor)
    else:
        print('already exists')
        return 'already exists'


def edit_user(username, password, new_password):
    user = m.User.load_user_by_name(cursor, username)
    print('edit user check password ', cl.check_password(password, user.hashed_password))
    if user is None:
        print('no such a user')
        return
    if not cl.check_password(password, user.hashed_password):
        print('password incorrect!, cannot edit')
        return
    if len(new_password) < 8:
        print('new password too short')
        return
    # that's the error here:
    # hashed_pass = cl.hash_password(args.password, None)
    # user.hashed_password = hashed_password
    # that's the correct version:
    user.hashed_password = new_password

    user.safe_to_db(cursor)


def delete_user(username, password):
    user = m.User.load_user_by_name(cursor, username)
    print('hashed password ', user)
    if user is None:
        print('no such a user to delete')
        return
    if not cl.check_password(password, user._hashed_password):
        print('password incorrect! can"t delete')
        return
    user.delete(cursor)


def list_users():
    for row in m.User.load_all_users(cursor):
        print(row)


if args.username is not None and args.password is not None and args.new_password is None and args.edit is None and args.list is None and args.delete is None:
    create_user(args.username, args.password)
elif args.username is not None and args.password is not None and args.new_password is not None and args.edit is not None and args.list is None and args.delete is None:
    edit_user(args.username, args.password, args.new_password)
elif args.username is not None and args.password is not None and args.new_password is None and args.edit is None and args.list is None and args.delete is not None:
    delete_user(args.username, args.password)
elif args.username is None and args.password is None and args.new_password is None and args.edit is None and args.list is not None and args.delete is None:
    list_users()
else:
    parser.print_help()
