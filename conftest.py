import pytest
import os 
from django.conf import settings
from pytest_factoryboy import register

from core.tests.factories import SeriesFactory, TagFactory
from blog.tests.factories import PostFactory
from recipe.tests.factories import RecipeFactory

register(TagFactory)
register(SeriesFactory)
register(PostFactory)
register(RecipeFactory)

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
