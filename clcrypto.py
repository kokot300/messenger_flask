#!/usr/bin/python

import hashlib
import random
from string import ascii_uppercase, ascii_lowercase, digits

ALPHABET = ascii_uppercase + ascii_lowercase + digits

def hash_password(password, salt=None):
    """
    Hashes the password with salt as an optional parameter.

    If salt is not provided, generates random salt.
    If salt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.

    :param str password: password to hash
    :param str salt: salt to hash, default None

    :rtype: str
    :return: hashed password
    """
    print('*' * 20, 'hash_password')
    print('hash_password salt ', salt)
    if salt == '':
        salt = None

    # generate salt if not provided
    if salt is None:
        salt = generate_salt()

    # fill to 16 chars if too short
    if len(salt) < 16:
        salt += ("a" * (16 - len(salt)))

    # cut to 16 if too long
    if len(salt) > 16:
        salt = salt[:16]

    # use sha256 algorithm to generate hash
    t_sha = hashlib.sha256()
    print('t_sha', t_sha)

    # we have to encode salt & password to utf-8, this is required by the
    # hashlib library.
    t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))
    print('salt ', salt)
    # return salt & hash joined
    print(salt, ' ', t_sha.hexdigest())
    return salt + t_sha.hexdigest()


def check_password(pass_to_check, hashed):
    """
    Checks the password.
    The function does the following:
        - gets the salt + hash joined,
        - extracts salt and hash,
        - hashes `p
        ass_to_check` with extracted salt,
        - compares `hashed` with hashed `pass_to_check`.
        - returns True if password is correct, or False. :)

    :param str pass_to_check: not hashed password
    :param str hashed: hashed password

    :rtype: bool
    :return: True if password is correct, False elsewhere
    """
    print('*' * 20, 'check_password')
    # extract salt
    salt = hashed[:16]
    print('salt ', salt)

    # extract hash to compare with
    hash_to_check = hashed[16:]
    print('hash to check ', hash_to_check)

    # hash password with extracted salt
    new_hash = hash_password(pass_to_check, salt)
    print('new_hash ', new_hash)
    print('new hash in cl ', new_hash)

    # compare hashes. If equal, return True
    return new_hash[16:] == hash_to_check


def generate_salt():
    """
    Generates a 16-character random salt.

    :rtype: str
    :return: str with generated salt
    """
    print('*' * 20, 'genetrate_salt')
    salt = ""
    for i in range(0, 16):
        # get a random element from the iterable
        salt += random.choice(ALPHABET)
    print(salt)
    return salt


if __name__ == '__main__':
    a = hash_password('abcabcabc', '1234567890123456')
    # a = 'OzqglAewRNYsZZdY9292b60235f7abb339411270313c4281c831fd447f82bd1c8bb4f6f8b371fdf8'
    print(a)
    bl = check_password('abcabcabc', a)
    print(bl)
