from sqlalchemy import (
    Column,
    Index,
    Unicode,
    UnicodeText,
    Integer,
    Text,
)
from ..security import (check_password, hash_password)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    name = Column(UnicodeText, nullable=True)

    def verify_password(self, password):
        if password == self.password:
            self.set_password(password)
        return check_password(password, self.password)

    def set_password(self, password):
        password_hash = hash_password(password)
        self.password = password_hash

    def get_author(self):
        return self.name if self.name else self.username


Index('user_username_index', User.username, unique=True, mysql_length=255)
