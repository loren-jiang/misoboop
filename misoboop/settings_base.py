"""
Shared base settings for misoboop project.
"""

import os
from django.templatetags.static import static as django_static

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('MB_SECRET_KEY')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]
INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition
INSTALLED_APPS = [
    'filebrowser',  # todo: maybe add later
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    'django.contrib.sitemaps',
    'django_extensions',
    'storages',
    'tinymce',
    'sorl.thumbnail',
    'newsletter',  # todo: for sure add later
    'threadedcomments',  # todo: probs add later
    'django_comments',  # needed for threaded comments
    'django_filters',
    'star_ratings',
    'debug_toolbar',  # don't use for production
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'misoboop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'misoboop.wsgi.application'


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

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

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

# AWS settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_CLOUDFRONT_DOMAIN')  # use cloudfront

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# s3 static settings
STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
#The file storage engine to use when collecting static files with the collectstatic management command.
STATICFILES_STORAGE = 'misoboop.storage_backends.CachedS3Boto3Storage'

# s3 public media settings
AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'misoboop.storage_backends.PublicMediaStorage'

AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'misoboop.storage_backends.PrivateMediaStorage'

# django-compressor settings
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE


# case-insensitive when looking up tags
TAGGIT_CASE_INSENSITIVE = True

BREADCRUMBS_TEMPLATE = "breadcrumbs.html"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ]
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}


SITE_ID = 1

# STAR_RATINGS_STAR_SPRITE = STATIC_URL + "assets/dumpling_sprite_sm.png"
STAR_RATINGS_ANONYMOUS = True

LIBSASS_OUTPUT_STYLE = 'nested'

LIBSASS_CUSTOM_FUNCTIONS = {
    'static': django_static,
    'map': lambda mapping, key: mapping.get(key),
}

COMPRESS_CSS_FILTERS = [
    'django_compressor_autoprefixer.AutoprefixerFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
    ('text/browserify', 'browserify -e {infile} -o {outfile}'),
)


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

X_FRAME_OPTIONS = 'sameorigin'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1;11211',
    }
}

THUMBNAIL_FORCE_OVERWRITE = True  # https://github.com/jazzband/sorl-thumbnail/issues/351