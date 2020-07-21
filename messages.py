#!/usr/bin/python

from argparse import ArgumentParser
import models as m
import clcrypto as cl
from psycopg2 import connect

parser = ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="receiver")
parser.add_argument("-s", "--send", help="text of message")
parser.add_argument("-l", "--list", help="all messages of user", action='count')

args = parser.parse_args()


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


def check_pass(username, password):
    u = m.User.load_user_by_name(cursor, username)
    if u is None:
        print('no such a user')
        return 'no such a user'
    if not cl.check_password(password, u._hashed_password):
        print('wrong password')
        return 'wrong password'
    return 0


def list_messages(username, password):
    if check_pass(username, password) == 0:
        u1 = m.User.load_user_by_name(cursor, username)
        your_messages = m.Messages.load_all_messages(cursor, u1.id)
        for row in your_messages:
            print(row)
    else:
        print('something went wrong…')


def send_message(username, password, to, send):
    if check_pass(username, password) == 0:
        u1 = m.User.load_user_by_name(cursor, username)
        u2 = m.User.load_user_by_name(cursor, to)
        mess = m.Messages(u1.id, u2.id, send)
        mess.safe_to_db(cursor)


if args.username is not None and args.password is not None and args.to is not None and args.send is not None and args.list is None:
    send_message(args.username, args.password, args.to, args.send)
elif args.username is not None and args.password is not None and args.to is None and args.send is None and args.list is not None:
    list_messages(args.username, args.password)
else:
    parser.print_help()
