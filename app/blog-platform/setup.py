import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid == 1.10.4',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'waitress',
    'alembic',
    'pyramid_retry',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'bcrypt',
    'passlib',
    'webhelpers2',
    'wtforms',
    'paginate_sqlalchemy',
    'psycopg2-binary',
    'supervisor',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest >= 3.7.4',
    'pytest-cov',
]

lint_require = [
    'flake8',
]

build_require = [
]

develop_require = [
    'cookiecutter',
    *build_require,
    *tests_require,
    *lint_require,
]

setup(
    name='blog_platform',
    version='0.0',
    description='Blog Platform',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
        'linting': lint_require,
        'develop': develop_require,
        'build': build_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = blog_platform:main',
        ],
        'console_scripts': [
            'initialize_blog_platform_db=blog_platform.scripts.initialize_db:main',
        ],
    },
)
