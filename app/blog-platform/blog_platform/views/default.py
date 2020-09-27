from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from ..models.user import User
from ..models.form_registration import RegistrationForm
from ..services.post import PostService
from ..services.user import UserService


@view_config(route_name='index', renderer='../templates/index.jinja2')
def index(request):
    user = UserService.by_id(request.authenticated_userid, request=request)
    page = int(request.params.get('page', 1))
    count = int(request.params.get('count', 5))
    paginator = PostService.get_paginator(request, page, count)
    return {'paginator': paginator, 'project': 'Kanava14.fi', 'user': user}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='login', renderer='string', request_method='POST')
def login(request):
    username = request.POST.get('username')
    headers = forget(request)
    if username:
        user = UserService.by_username(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.id)
    return HTTPFound(location=request.route_url('index'), headers=headers)


@view_config(route_name='logout', renderer='string')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('index'), headers=headers)


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(username=form.username.data, name=form.name.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('index'))
    return {'form': form}
