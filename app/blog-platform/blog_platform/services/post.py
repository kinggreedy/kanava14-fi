import sqlalchemy as sa
from paginate_sqlalchemy import SqlalchemyOrmPage

from ..models.post import Post
from ..models.user import User


class PostService(object):
    @classmethod
    def all(cls, request):
        query = request.dbsession.query(Post)
        return query.order_by(sa.desc(Post.created))

    @classmethod
    def by_id(cls, _id, request):
        query = request.dbsession.query(Post)
        return query.get(_id)

    @classmethod
    def get_paginator(cls, request, page=1, count=5):
        count = max(1, min(count, 20))
        query = request.dbsession.query(Post, User).join(User)
        query = query.order_by(sa.desc(Post.created))
        try:
            query_params = request.GET.mixed()
        except AttributeError:
            # When using DummySession from pytest
            # it's dict instead of webob.multidict
            query_params = request.GET

        def url_maker(link_page):
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return SqlalchemyOrmPage(query, page, items_per_page=count,
                                 url_maker=url_maker)
