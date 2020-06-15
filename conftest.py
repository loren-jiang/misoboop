import pytest
import os 
import shutil
from django.conf import settings
from pytest_factoryboy import register

from core.tests.factories import SeriesFactory, TagFactory
from blog.tests.factories import PostFactory
from recipe.tests.factories import RecipeFactory

register(TagFactory)
register(SeriesFactory)
register(PostFactory)
register(RecipeFactory)


@pytest.fixture
def ten_posts(post_factory):
    return [post_factory() for _ in range(10)]

@pytest.fixture
def ten_seriess(series_factory):
    return [series_factory() for _ in range(10)]

@pytest.fixture
def ten_recipes(recipe_factory):
    return [recipe_factory() for _ in range(10)]

def pytest_sessionstart(session):
    print("\ntesting started")

    if (settings.MEDIA_ROOT == "_temp"):
        os.mkdir('_temp')

def pytest_sessionfinish(session, exitstatus):
    print("\ntesting concluded")
    # delete _temp directory after testing
    # if (settings.MEDIA_ROOT == "_temp"):
    #     shutil.rmtree("_temp")

# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv('MB_DB_NAME'),
#         'USER': os.getenv('MB_DB_USER'),
#         'PASSWORD': os.getenv('MB_DB_PASSWORD'),
#         'HOST': os.getenv('MB_DB_HOST'),
#         'PORT': os.getenv('MB_DB_PORT'),
#     }
