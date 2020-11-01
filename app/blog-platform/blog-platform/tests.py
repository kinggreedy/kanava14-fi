import unittest

from pyramid import testing
import unittest.mock as mock

import transaction


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestInitializeDBSuccess(BaseTest):
    def setUp(self):
        super(TestInitializeDBSuccess, self).setUp()
        self.init_database()
        from .scripts import initialize_db
        initialize_db.setup_models(dbsession=self.session)

    def test_ensure_no_project_error(self):
        from .views.default import index
        dummy_request = testing.DummyRequest(dbsession=self.session)
        info = index(dummy_request)
        self.assertTrue("status_int" not in info or info.status_int == 200)


class TestViewIndex(BaseTest):
    def setUp(self):
        super(TestViewIndex, self).setUp()
        self.init_database()
        self.config.add_route('index', '/')
        from .models import User
        from .security import hash_password
        user = User(id=2,
                    username=u"user_test",
                    password=hash_password(u"user_test"),
                    name=u"User Test")
        self.session.add(user)

    def test_passing_view(self):
        from .views.default import index
        dummy_request = testing.DummyRequest(dbsession=self.session)
        info = index(dummy_request)
        self.assertEqual(info['project'], 'Kanava14.fi')

    def test_login(self):
        from .views.default import login
        from webob.multidict import MultiDict
        from pyramid.httpexceptions import HTTPFound

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('username', 'user_test'),
                ('password', 'user_test'),
            ])
        )
        info = login(dummy_request)
        self.assertIsInstance(info, HTTPFound)

    def test_login_unavailable_username(self):
        from .views.default import login
        from webob.multidict import MultiDict

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('username', 'user_wrongusername'),
                ('password', 'user_pw'),
            ])
        )
        info = login(dummy_request)
        self.assertIn("Wrong username or password",
                      info['form'].password.errors)

    def test_login_wrong_password(self):
        from .views.default import login
        from webob.multidict import MultiDict

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('username', u'user_test'),
                ('password', u'user_wrongpw'),
            ])
        )
        info = login(dummy_request)
        self.assertIn("Wrong username or password",
                      info['form'].password.errors)

    def test_logout(self):
        from .views.default import logout
        from pyramid.httpexceptions import HTTPFound

        self.config.testing_securitypolicy(userid=1)
        dummy_request = testing.DummyRequest(dbsession=self.session)
        info = logout(dummy_request)
        self.assertIsInstance(info, HTTPFound)


class TestUnitIndexViewPagination(BaseTest):
    def setUp(self):
        super(TestUnitIndexViewPagination, self).setUp()
        self.init_database()
        self.config.add_route('index', '/')

        from .models import Post, User
        author = User(id=2,
                      username="author_test",
                      password="author_test",
                      name="Author Test")
        self.session.add(author)
        for i in range(23):
            str_i = str(i)
            blog = Post(title="Test Title " + str_i,
                        body="Test Content " + str_i,
                        author=author.id)
            self.session.add(blog)
        match_route = mock.Mock()
        match_route.name = "index"
        self.match_route = match_route

    def test_custom_link_tag_render_default(self):
        from .views.default import index
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            path='/',
            matched_route=self.match_route,
        )
        info = index(dummy_request)
        paginator = info['paginator']
        custom_link_tag = info['custom_link_tag']
        render_str = paginator.pager(
            format='$link_previous~2~$link_next',
            curpage_attr={'state': 'active'},
            dotdot_attr={'state': 'disabled'},
            symbol_previous='Previous',
            symbol_next='Next',
            link_tag=custom_link_tag
        )
        render_expected = '''\
<li class="page-item active"><span class=" page-link" state="active">\
1</span></li> <li class="page-item"><a class="page-link" href="/?page\
=2">2</a></li> <li class="page-item"><a class="page-link" href="/?pag\
e=3">3</a></li> <li class="page-item disabled"><span class=" page-lin\
k" state="disabled">..</span></li> <li class="page-item"><a class="pa\
ge-link" href="/?page=5">5</a></li><li class="page-item"><a class="pa\
ge-link" href="/?page=2">Next</a></li>\
'''
        self.assertEqual(render_str, render_expected)

    def test_custom_link_tag_render_page1(self):
        from .views.default import index
        from webob.multidict import MultiDict
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            path='/?page=1',
            matched_route=self.match_route,
            params=MultiDict([
                ('page', 1),
            ]),
        )
        info = index(dummy_request)
        paginator = info['paginator']
        custom_link_tag = info['custom_link_tag']
        render_str = paginator.pager(
            format='$link_previous~2~$link_next',
            curpage_attr={'state': 'active'},
            dotdot_attr={'state': 'disabled'},
            symbol_previous='Previous',
            symbol_next='Next',
            link_tag=custom_link_tag
        )
        render_expected = '''\
<li class="page-item active"><span class=" page-link" state="active">\
1</span></li> <li class="page-item"><a class="page-link" href="/?page\
=2">2</a></li> <li class="page-item"><a class="page-link" href="/?pag\
e=3">3</a></li> <li class="page-item disabled"><span class=" page-lin\
k" state="disabled">..</span></li> <li class="page-item"><a class="pa\
ge-link" href="/?page=5">5</a></li><li class="page-item"><a class="pa\
ge-link" href="/?page=2">Next</a></li>\
'''
        self.assertEqual(render_str, render_expected)

    def test_custom_link_tag_render_page2(self):
        from .views.default import index
        from webob.multidict import MultiDict
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            path='/?page=1',
            matched_route=self.match_route,
            params=MultiDict([
                ('page', 2),
            ]),
        )
        info = index(dummy_request)
        paginator = info['paginator']
        custom_link_tag = info['custom_link_tag']
        render_str = paginator.pager(
            format='$link_previous~2~$link_next',
            curpage_attr={'state': 'active'},
            dotdot_attr={'state': 'disabled'},
            symbol_previous='Previous',
            symbol_next='Next',
            link_tag=custom_link_tag
        )
        render_expected = '''\
<li class="page-item"><a class="page-link" href="/?page=1">Previous</\
a></li><li class="page-item"><a class="page-link" href="/?page=1">1</\
a></li> <li class="page-item active"><span class=" page-link" state="\
active">2</span></li> <li class="page-item"><a class="page-link" href\
="/?page=3">3</a></li> <li class="page-item"><a class="page-link" hre\
f="/?page=4">4</a></li> <li class="page-item"><a class="page-link" hr\
ef="/?page=5">5</a></li><li class="page-item"><a class="page-link" hr\
ef="/?page=3">Next</a></li>\
'''
        self.assertEqual(render_str, render_expected)

    def test_custom_link_tag_render_page2_count10(self):
        from .views.default import index
        from webob.multidict import MultiDict
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            path='/?page=1',
            matched_route=self.match_route,
            params=MultiDict([
                ('page', 2),
                ('count', 10),
            ]),
        )
        info = index(dummy_request)
        paginator = info['paginator']
        custom_link_tag = info['custom_link_tag']
        render_str = paginator.pager(
            format='$link_previous~2~$link_next',
            curpage_attr={'state': 'active'},
            dotdot_attr={'state': 'disabled'},
            symbol_previous='Previous',
            symbol_next='Next',
            link_tag=custom_link_tag
        )
        render_expected = '''\
<li class="page-item"><a class="page-link" href="/?page=1&count=10">P\
revious</a></li><li class="page-item"><a class="page-link" href="/?pa\
ge=1&count=10">1</a></li> <li class="page-item active"><span class=" \
page-link" state="active">2</span></li> <li class="page-item"><a clas\
s="page-link" href="/?page=3&count=10">3</a></li><li class="page-item\
"><a class="page-link" href="/?page=3&count=10">Next</a></li>\
'''
        self.assertEqual(render_str, render_expected)

    def test_custom_link_tag_render_lastpage(self):
        from .views.default import index
        from webob.multidict import MultiDict
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            path='/?page=1',
            matched_route=self.match_route,
            params=MultiDict([
                ('page', 5),
            ]),
        )
        info = index(dummy_request)
        paginator = info['paginator']
        custom_link_tag = info['custom_link_tag']
        render_str = paginator.pager(
            format='$link_previous~2~$link_next',
            curpage_attr={'state': 'active'},
            dotdot_attr={'state': 'disabled'},
            symbol_previous='Previous',
            symbol_next='Next',
            link_tag=custom_link_tag
        )
        render_expected = '''\
<li class="page-item"><a class="page-link" href="/?page=4">Previous</\
a></li><li class="page-item"><a class="page-link" href="/?page=1">1</\
a></li> <li class="page-item disabled"><span class=" page-link" state\
="disabled">..</span></li> <li class="page-item"><a class="page-link"\
 href="/?page=3">3</a></li> <li class="page-item"><a class="page-link\
" href="/?page=4">4</a></li> <li class="page-item active"><span clas\
s=" page-link" state="active">5</span></li>\
'''
        self.assertEqual(render_str, render_expected)


class TestViewRegister(BaseTest):
    def setUp(self):
        super(TestViewRegister, self).setUp()
        self.config.add_route('index', '/')
        self.config.add_route('register', '/register')
        self.init_database()

    def test_register_view(self):
        from .views.default import register
        dummy_request = testing.DummyRequest(dbsession=self.session)
        dummy_request.POST = None
        info = register(dummy_request)
        self.assertTrue("status_int" not in info or info.status_int == 200)

    def test_register_user(self):
        from .views.default import register
        from webob.multidict import MultiDict
        from pyramid.httpexceptions import HTTPFound
        from .models import User

        username = 'user'
        password = 'pass'
        name = 'name'

        policy = mock.Mock()
        policy.remember = mock.MagicMock(name='remember')

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('username', username),
                ('password', password),
                ('name', name)
            ]),
        )
        registry = dummy_request.registry
        registry.queryUtility = mock.Mock(return_value=policy)

        info = register(dummy_request)
        self.assertIsInstance(info, HTTPFound)
        user_db: User = self.session.query(User).get(1)
        policy.remember.assert_called_with(dummy_request, user_db.id)
        self.assertEqual(user_db.username, username)
        self.assertTrue(user_db.verify_password(password))
        self.assertFalse(user_db.verify_password("notpass"))
        self.assertEqual(user_db.name, name)
        self.assertEqual(user_db.get_author(), name)

    def test_register_user_without_name(self):
        from .views.default import register
        from webob.multidict import MultiDict
        from pyramid.httpexceptions import HTTPFound
        from .models import User
        username = 'user'
        password = 'pass'
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('username', username),
                ('password', password),
            ])
        )
        info = register(dummy_request)
        self.assertIsInstance(info, HTTPFound)
        user_db: User = self.session.query(User).get(1)
        self.assertEqual(user_db.username, username)
        self.assertTrue(user_db.verify_password(password))
        self.assertFalse(user_db.verify_password("notpass"))
        self.assertEqual(user_db.name, None)
        self.assertEqual(user_db.get_author(), username)

    def test_register_unsecure_password(self):
        from .views.default import register
        from webob.multidict import MultiDict
        username = 'user'
        password = 'p'
        name = 'name'
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('username', username),
                ('password', password),
                ('name', name)
            ])
        )
        info = register(dummy_request)
        self.assertIn("Field must be at least 3 characters long.",
                      info['form'].password.errors)

    def test_register_unavailable_username(self):
        from .views.default import register
        from webob.multidict import MultiDict
        from .models import User
        from .security import hash_password

        username = 'user_test'
        password = 'pass'
        name = 'name'
        user = User(id=2,
                    username=username,
                    password=hash_password(u"user_test"),
                    name=u"User Test")
        self.session.add(user)

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('username', username),
                ('password', password),
                ('name', name)
            ])
        )
        info = register(dummy_request)
        self.assertIn("Username is not available",
                      info['form'].username.errors)


class TestUnitForm(unittest.TestCase):
    def test_update_post_form(self):
        from .models.form_blogpost import BlogPostFormUpdate
        from webob.multidict import MultiDict
        blog_id = 3
        title = "Blog Title"
        body = "Blog Body"
        form = BlogPostFormUpdate(MultiDict([
            ('id', 3),
            ('title', title),
            ('body', body)
        ]))
        self.assertEqual(form.id.data, blog_id)
        self.assertEqual(form.title.data, title)
        self.assertEqual(form.body.data, body)


class TestUnitPost(unittest.TestCase):
    def test_post_review_content_short(self):
        from .models import Post
        title = "Test Title"
        body = "Test Content short"
        expected_preview = "Test Content short"
        blog = Post(title=title, body=body)
        self.assertEqual(blog.preview_content, expected_preview)

    def test_post_review_content_long(self):
        from .models import Post
        title = "Test Title"
        body = "In every industry, we hear about the struggle " \
               "to transform from a reactive to proactive " \
               "organization that"
        expected_preview = "In every industry, we hear about the struggle " \
                           "to transform from a reactive to proactive ..."
        blog = Post(title=title, body=body)
        self.assertEqual(blog.preview_content, expected_preview)

    def test_post_review_content_with_invalid_words(self):
        from .models import Post
        title = "Test Title"
        body = "Know your customers like never before\n" \
               "-------------------------------------\n" \
               "In every industrywehearabout the struggle " \
               "to transform from a reactive to proactive " \
               "organization that"
        expected_preview = "Know your customers like never before " \
                           "In every industryweheara the struggle " \
                           "to transform from a ..."
        blog = Post(title=title, body=body)
        self.assertEqual(blog.preview_content, expected_preview)

    def test_post_created_in_words(self):
        from .models import Post
        from datetime import datetime, timezone
        title = "Test Title"
        body = "Test Content"
        dt = datetime(2020, 8, 15, 15, 16, 17, 345, tzinfo=timezone.utc)
        blog = Post(title=title, body=body, created=dt)
        self.assertEqual(blog.created_in_words, "August 15, 2020")

    def test_post_edited_in_words(self):
        from .models import Post
        from datetime import datetime, timedelta
        title = "Test Title"
        body = "Test Content"
        dt = datetime.utcnow() - timedelta(seconds=1,
                                           minutes=2,
                                           hours=3,
                                           days=4)
        blog = Post(title=title, body=body, edited=dt)
        self.assertEqual(blog.edited_in_words, "4 days, 3 hours and 2 minutes")

    def test_post_get_language_name(self):
        from .models import Post
        title = "Test Title"
        body = "Test Content"
        blog = Post(title=title, body=body, lang="en")
        self.assertEqual(blog.get_language_name, "English")


class TestViewPostBlog(BaseTest):
    def setUp(self):
        super(TestViewPostBlog, self).setUp()
        self.init_database()

        from .models import Post, User
        author = User(id=2,
                      username="author_test",
                      password="author_test",
                      name="Author Test")
        blog = Post(id=2,
                    title="Test Title",
                    body="Test Content",
                    author=author.id)
        self.session.add(author)
        self.session.add(blog)
        self.author = author
        self.blog = blog

    def test_post_view(self):
        from .views.post import post_view
        from webob.multidict import MultiDict

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            matchdict=MultiDict([
                ('id', self.blog.id)
            ])
        )
        info = post_view(dummy_request)
        self.assertEqual(info['entry'], self.blog)
        self.assertEqual(info['author'], self.author)

    def test_post_view_unexist_blog(self):
        from .views.post import post_view
        from webob.multidict import MultiDict
        from pyramid.httpexceptions import HTTPNotFound

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            matchdict=MultiDict([
                ('id', self.blog.id + 1)
            ])
        )
        info = post_view(dummy_request)
        self.assertIsInstance(info, HTTPNotFound)

    def test_post_create_get(self):
        from .views.post import post_create
        from webob.multidict import MultiDict
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([]),
        )
        info = post_create(dummy_request)
        from .models.form_blogpost import BlogPostFormCreate
        self.assertIsInstance(info['form'], BlogPostFormCreate)

    def test_post_create_post(self):
        from .views.post import post_create
        from webob.multidict import MultiDict
        from .models import Post
        from pyramid.httpexceptions import HTTPFound

        title = "Test Title"
        body = "Test Content"
        self.config.testing_securitypolicy(userid=self.author.id)
        self.config.add_route('index', '/')

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('title', title),
                ('body', body),
            ]),
        )

        info = post_create(dummy_request)
        blog_db: Post = self.session.query(Post).get(self.blog.id + 1)
        self.assertIsInstance(info, HTTPFound)
        self.assertEqual(blog_db.title, title)
        self.assertEqual(blog_db.body, body)
        self.assertEqual(blog_db.author, self.author.id)
        self.assertIsNotNone(blog_db.created)
        self.assertIsNone(blog_db.edited)

    # FIXME: FE functional test: test_post_create_post_without_login

    def test_post_update_post(self):
        from .views.post import post_update
        from webob.multidict import MultiDict
        from .models import Post
        from pyramid.httpexceptions import HTTPFound

        title = "Test Title2"
        body = "Test Content2"
        self.config.testing_securitypolicy(userid=self.author.id)
        self.config.add_route(
            'post',
            r'/post/{id:\d+}/{slug}',
            factory='blog_platform.security.PostFactory'
        )

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('title', title),
                ('body', body),
            ]),
            params=MultiDict([
                ('id', self.blog.id),
            ]),
        )

        info = post_update(dummy_request)
        blog_db: Post = self.session.query(Post).get(self.blog.id)
        self.assertIsInstance(info, HTTPFound)
        self.assertEqual(blog_db.title, title)
        self.assertEqual(blog_db.body, body)
        self.assertEqual(blog_db.author, self.author.id)
        self.assertIsNotNone(blog_db.created)
        # FIXME: self.assertIsNotNone(blog_db.edited)

    def test_post_update_hijack(self):
        from .views.post import post_update
        from webob.multidict import MultiDict
        from .models import Post, User
        from pyramid.httpexceptions import HTTPForbidden

        author = User(id=3,
                      username="author_test_2",
                      password="author_test_2",
                      name="Author Test 2")
        self.session.add(author)
        title = "Test Title Edited"
        body = "Test Content Edited"
        self.config.testing_securitypolicy(userid=author.id)
        self.config.add_route(
            'post',
            r'/post/{id:\d+}/{slug}',
            factory='blog_platform.security.PostFactory'
        )

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
            post=MultiDict([
                ('title', title),
                ('body', body),
            ]),
            params=MultiDict([
                ('id', self.blog.id),
            ]),
        )

        info = post_update(dummy_request)
        blog_db: Post = self.session.query(Post).get(self.blog.id)

        self.assertIsInstance(info, HTTPForbidden)
        self.assertEqual(blog_db.title, self.blog.title)
        self.assertEqual(blog_db.body, self.blog.body)
        self.assertEqual(blog_db.author, self.author.id)
        self.assertNotEqual(blog_db.title, title)
        self.assertNotEqual(blog_db.body, body)
        self.assertNotEqual(blog_db.author, author.id)
        self.assertIsNotNone(blog_db.created)
        self.assertIsNone(blog_db.edited)


class TestBlogLanguageDetection(BaseTest):
    def setUp(self):
        super(TestBlogLanguageDetection, self).setUp()
        self.init_database()
        from .models import Post, User
        author = User(id=2,
                      username="author_test",
                      password="author_test",
                      name="Author Test")
        blog = Post(id=2,
                    title="Test Title",
                    body="Hello World",
                    author=author.id)
        self.session.add(author)
        self.session.add(blog)
        self.author = author
        self.blog = blog

    def test_demo_detect_language(self):
        from .tasks.blog_post_tasks import detect_language
        from .models import Post
        dummy_request = testing.DummyRequest(
            dbsession=self.session,
        )
        detect_language(dummy_request, "demo")
        blog_db = self.session.query(Post).get(self.blog.id)

        self.assertEqual(blog_db.lang, "en")
        self.assertIsNotNone(blog_db.lang_timestamp)

    def test_demo_detect_language_without_apikey(self):
        from .models import Post
        from .tasks.blog_post_tasks import detect_language

        dummy_request = testing.DummyRequest(
            dbsession=self.session,
        )
        detect_language(dummy_request, "")
        blog_db = self.session.query(Post).get(self.blog.id)

        self.assertIsNone(blog_db.lang)
        self.assertIsNone(blog_db.lang_timestamp)

        detect_language(dummy_request, "__languagedetectorapikey__")
        blog_db = self.session.query(Post).get(self.blog.id)

        self.assertIsNone(blog_db.lang)
        self.assertIsNone(blog_db.lang_timestamp)
