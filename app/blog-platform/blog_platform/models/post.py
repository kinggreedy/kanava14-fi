from sqlalchemy import (
    Column,
    Unicode,
    UnicodeText,
    Integer,
    DateTime,
    ForeignKey,
)

import datetime
from webhelpers2.text import urlify
from webhelpers2.date import distance_of_time_in_words

from .meta import Base
from .user import User


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, onupdate=datetime.datetime.utcnow)
    author = Column(
        Integer,
        ForeignKey(User.__tablename__ + ".id"),
        nullable=False
    )

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return self.created.strftime("%B %d, %Y")

    @property
    def edited_in_words(self):
        return None if self.edited is None \
            else distance_of_time_in_words(self.edited,
                                           datetime.datetime.utcnow(),
                                           granularity='minute')

    @property
    def preview_content(self):
        return self.body
