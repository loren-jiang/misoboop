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
# INSTALLED_APPS = [
#     'filebrowser',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sites',
#     'django_extensions',
#     'storages',
#     'tinymce',
#     'sorl.thumbnail',
#     'newsletter',
#     'threadedcomments',
#     'django_comments',
#     'django_filters',
#     'star_ratings',
#     'debug_toolbar',
#     'rest_framework',
#     'django_json_ld',
#     'adminsortable',
#     'compressor',
#     'django_bootstrap_breadcrumbs',
#     'taggit',
#     'taggit_serializer',
#     'recipe',
#     'core',
#     'blog'
# ]
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'recipe/static'),
    os.path.join(BASE_DIR, 'blog/static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',  # for sass
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' #default settings


DEBUG_TOOLBAR_CONFIG = {
    # 'SHOW_TOOLBAR_CALLBACK': lambda r: False,  # disables it
}

