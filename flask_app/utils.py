import hashlib


def get_password_hash(user, password):
    salt = user.login + user.id
    hashlib.sha256(password + salt).hexdigest()
