from models import User


def create_user(name):
    return User(name)


class UserRepository(object):
    pass