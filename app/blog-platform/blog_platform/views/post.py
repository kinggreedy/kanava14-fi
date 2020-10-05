from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPForbidden

from ..models.post import Post
from ..models.form_blogpost import BlogPostFormCreate, BlogPostFormUpdate
from ..services.post import PostService
from ..services.user import UserService


@view_config(route_name='post', renderer='../templates/post/view.jinja2',
             permission='view')
def post_view(request):
    blog_id = int(request.matchdict.get('id', -1))
    entry = PostService.by_id(blog_id, request)
    author = UserService.by_id(entry.author, request)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry, 'author': author}


@view_config(route_name='post_action', match_param='action=create',
             renderer='../templates/post/edit.jinja2', permission='create')
def post_create(request):
    user = UserService.by_id(request.authenticated_userid, request=request)
    entry = Post()
    form = BlogPostFormCreate(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.author = user.id
        request.dbsession.add(entry)
        return HTTPFound(location=request.route_path('index'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='post_action', match_param='action=edit',
             renderer='../templates/post/edit.jinja2', permission='edit')
def post_update(request):
    user = UserService.by_id(request.authenticated_userid, request=request)
    blog_id = int(request.params.get('id', -1))
    entry = PostService.by_id(blog_id, request)
    if not entry:
        return HTTPNotFound()
    if entry.author != user.id:
        return HTTPForbidden()

    form = BlogPostFormUpdate(request.POST, entry)
    if request.method == 'POST' and form.validate():
        del form.id
        form.populate_obj(entry)
        return HTTPFound(
            location=request.route_path('post', id=entry.id, slug=entry.slug))
    return {'form': form, 'action': request.matchdict.get('action')}
