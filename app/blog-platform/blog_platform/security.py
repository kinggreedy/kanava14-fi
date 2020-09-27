from pyramid.security import Allow, Authenticated
import bcrypt


def hash_password(password):
    pwhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def check_password(password, hashed_password):
    expected_hash = hashed_password.encode('utf8')
    return bcrypt.checkpw(password.encode('utf8'), expected_hash)


class PostFactory(object):
    __acl__ = [(Allow, Authenticated, 'view'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'), ]

    def __init__(self, request):
        pass
