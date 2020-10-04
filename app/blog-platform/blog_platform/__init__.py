from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authentication_policy = AuthTktAuthenticationPolicy(
        settings['userauthentication.secret'],
        hashalg='sha512'
    )
    authorization_policy = ACLAuthorizationPolicy()
    session_factory = SignedCookieSessionFactory(
        settings['userauthentication.secret']
    )

    with Configurator(settings=settings,
                      authentication_policy=authentication_policy,
                      authorization_policy=authorization_policy,
                      session_factory=session_factory) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        config.add_request_method(get_user, 'user', reify=True)

    return config.make_wsgi_app()


def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        from .services.user import UserService
        return UserService.by_id(user_id, request)
