from ..models.user import User


class UserService(object):
    @classmethod
    def by_username(cls, username, request):
        return request.dbsession\
            .query(User)\
            .filter(User.username == username)\
            .first()

    @classmethod
    def by_id(cls, id, request):
        return request.dbsession.query(User).filter(User.id == id).first()
