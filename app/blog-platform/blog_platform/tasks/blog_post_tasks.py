from pyramid_celery import celery_app as app
from ..services.post import PostService
import detectlanguage
from pyramid import testing
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


@app.task
def detect_language_task():
    engine = create_engine(
        app.conf['PYRAMID_REGISTRY'].settings["sqlalchemy.url"],
        convert_unicode=True,
        pool_recycle=3600, pool_size=10
    )
    db_session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))

    request = testing.DummyRequest(dbsession=db_session)
    result = detect_language(
        request,
        app.conf['PYRAMID_REGISTRY'].settings["languagedetector.apikey"]
    )
    db_session.commit()
    return result


def detect_language(request, api_key):
    detectlanguage.configuration.api_key = api_key
    if (not api_key) or (api_key == '__languagedetectorapikey__'):
        return 0

    posts = PostService.missing_language(request)
    print("Processing", len(posts), "posts")
    for post in posts:
        lang = detectlanguage.detect(post.body)
        if lang[0]["isReliable"]:
            post.lang = lang[0]["language"]
            post.lang_timestamp = datetime.utcnow()

    return 0
