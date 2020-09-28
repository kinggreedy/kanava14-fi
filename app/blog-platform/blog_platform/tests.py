import unittest

from pyramid import testing

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


class TestIndexViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestIndexViewSuccessCondition, self).setUp()
        self.init_database()

    def test_passing_view(self):
        from .views.default import index
        dummy_request = testing.DummyRequest(dbsession=self.session)
        info = index(dummy_request)
        self.assertEqual(info['project'], 'Kanava14.fi')


class TestRegisterView(BaseTest):
    def setUp(self):
        super(TestRegisterView, self).setUp()
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
        username = 'user'
        password = 'pass'
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
        from pyramid.httpexceptions import HTTPFound
        self.assertIsInstance(info, HTTPFound)


class TestForm(unittest.TestCase):
    def test_update_post_form(self):
        from .models.form_blogpost import BlogPostFormUpdate
        from webob.multidict import MultiDict
        id = 3
        title = "Blog Title"
        body = "Blog Body"
        form = BlogPostFormUpdate(MultiDict([
            ('id', 3),
            ('title', title),
            ('body', body)
        ]))
        self.assertEqual(form.id.data, id)
        self.assertEqual(form.title.data, title)
        self.assertEqual(form.body.data, body)
