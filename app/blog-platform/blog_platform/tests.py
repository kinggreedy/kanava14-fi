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


class TestMyViewSuccessCondition(BaseTest):
    def setUp(self):
        super(TestMyViewSuccessCondition, self).setUp()
        self.init_database()

    def test_passing_view(self):
        from .views.default import index
        dummy_request = testing.DummyRequest(dbsession=self.session)
        info = index(dummy_request)
        self.assertEqual(info['project'], 'Kanava14.fi')


class TestForm(unittest.TestCase):
    def test_update_post_form(self):
        from .models.form_blogpost import BlogPostFormUpdate
        from webob.multidict import MultiDict
        form = BlogPostFormUpdate(MultiDict([
            ('id', 3),
            ('title', "Blog Title"),
            ('body', "Blog Body")
        ]))
        self.assertEqual(form.id.data, 3)
        self.assertEqual(form.title.data, "Blog Title")
        self.assertEqual(form.body.data, "Blog Body")
