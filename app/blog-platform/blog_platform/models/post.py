from sqlalchemy import (
    Column,
    Unicode,
    UnicodeText,
    Integer,
    DateTime,
    ForeignKey,
)

import datetime
import re
from webhelpers2.text import urlify
from webhelpers2.date import distance_of_time_in_words
from iso_language_codes import language_name

from .meta import Base
from .user import User


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    body = Column(UnicodeText, default=u'')
    lang = Column(Unicode(255))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, onupdate=datetime.datetime.utcnow)
    lang_timestamp = Column(DateTime)
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
        return (
            None if self.edited is None
            else distance_of_time_in_words(self.edited,
                                           datetime.datetime.utcnow(),
                                           granularity='minute')
        )

    @property
    def preview_content(self):
        """
        Get Preview Content of a blog post

        Short content are based on the body of the blog post
        and any non words are removed. The word will also be
        trimmed down to 12 characters
        """
        list_words = self.body.split()
        collected_words = []
        count = 0
        max_words = 15
        for word in list_words:
            if re.sub(r'[^\w]', '', word) != "":
                collected_words.append(re.sub(r'[^\w\',."-]', '', word)[:15])
                count += 1
                if count >= max_words + 1:
                    break
        if count > max_words:
            collected_words[count - 1] = "..."

        return " ".join(collected_words)

    @property
    def get_language_name(self):
        return language_name(self.lang)
