"""
Django development settings overrides for misoboop project.
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# Application definition
INSTALLED_APPS = [
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'storages',
    'tinymce',
    'sorl.thumbnail',
    'newsletter',
    'threadedcomments',
    'django_comments',
    'django_filters',
    'star_ratings',
    'debug_toolbar',
    'rest_framework',
    'django_json_ld',
    'adminsortable',
    'compressor',
    'django_bootstrap_breadcrumbs',
    'taggit',
    'taggit_serializer',
    'recipe',
    'core',
    'blog'
]
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

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' #default settings

COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE


DEBUG_TOOLBAR_CONFIG = {}

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

LIBSASS_OUTPUT_STYLE = 'nested'
