import pytest
import os 
from django.conf import settings

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('MB_DB_NAME'),
        'USER': os.getenv('MB_DB_USER'),
        'PASSWORD': os.getenv('MB_DB_PASSWORD'),
        'HOST': os.getenv('MB_DB_HOST'),
        'PORT': os.getenv('MB_DB_PORT'),
    }
