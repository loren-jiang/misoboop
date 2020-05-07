"""
Django development settings for misoboop project.
"""
from .settings_base import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('MB_DB_NAME'),
        'USER': os.getenv('MB_DB_USER'),
        'PASSWORD': os.getenv('MB_DB_PASSWORD'),
        'HOST': os.getenv('MB_DB_HOST'),
        'PORT': os.getenv('MB_DB_PORT'),
    }
}

# Use local static files, and not cloudfront
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' #default settings

COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE


DEBUG_TOOLBAR_CONFIG = {}

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

