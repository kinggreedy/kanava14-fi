def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('post', r'/post/{id:\d+}/{slug}',
                     factory='blog_platform.security.PostFactory')
    config.add_route('post_action', '/post/{action}',
                     factory='blog_platform.security.PostFactory')
