from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
import transaction

from ..models.user import User
from ..models.form_registration import RegistrationForm, SignInForm
from ..services.post import PostService
from ..services.user import UserService


@view_config(route_name='index', renderer='../templates/index.jinja2')
def index(request):
    if request.authenticated_userid:
        request.session['user'] = UserService.by_id(
            request.authenticated_userid,
            request=request
        )
    page = int(request.params.get('page', 1))
    count = int(request.params.get('count', 5))
    paginator = PostService.get_paginator(request, page, count)
    return {'paginator': paginator, 'project': 'Kanava14.fi'}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    form = SignInForm(request.POST)
    if request.method == 'POST' and form.validate():
        username = request.POST.get('username')
        headers = forget(request)
        if username:
            user = UserService.by_username(username, request=request)
            if user and user.verify_password(request.POST.get('password')):
                headers = remember(request, user.id)
                request.session['user'] = user
        return HTTPFound(location=request.route_url('index'), headers=headers)
    return {'form': form}


@view_config(route_name='logout', renderer='string')
def logout(request):
    headers = forget(request)
    request.session['user'] = None
    return HTTPFound(location=request.route_url('index'), headers=headers)


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        # add user to database
        new_user = User(username=form.username.data, name=form.name.data)
        new_user.set_password(form.password.data)
        request.dbsession.add(new_user)
        transaction.commit()

        # put that registered user as logged in
        user = UserService.by_username(new_user.username, request=request)
        headers = remember(request, user.id)
        return HTTPFound(location=request.route_url('index'), headers=headers)
    return {'form': form}
