"""
Django settings for OpenAwards project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../apps')))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mvuzrok+)d1d@$y89n0y%$(lko)i72gqiw$9udrvbntlm2#zd('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


INSTALLED_APPS = [
    'apps.users.apps.UsersConfig',
    'apps.openawards.apps.OpenAwardsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'constance.backends.database',
    'constance',
    'storages'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OpenAwards.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'OpenAwards.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'openawards',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Andorra'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('ca', _('Catalan')),
    ('es', _('Spanish')),
]


# APPS
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTH_USER_MODEL = 'openawards.User'

DEV_SETTINGS_MODULE = 'OpenAwards.settings.dev'
USER_FIXTURE_FACTORY_CLASS = 'openawards.tests.fixtures.UserFactory'

# Constance
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'CREDITS_WHEN_CREATED': (5, 'Number of credits given to the user when they sign up', int),
    'ETIQUETTE_TEXT': ('# Etiquette!', 'Markdown text for etiquette page'),
    'AUTHORSHIP_CLAIM': (
        "If you are the author or owner of the rights of this work, and it appears listed under a "
        "different author's name, please fill this form and we'll get back to you to fix "
        "the situation.", 'Subtitle for this section.'),
    'WORK_AUTHORSHIP_TEXT': (
        "Are you the owner of this work, you have their permission, or the work license allow you to enroll it to these"
        "awards? [[ FULL TEXT PENDING ]]", "Work upload, explanation about authorship radio button."),
    'WORK_AUTHORSHIP_YES': (
        "Yes, I am the author, have permission, or the license authorizes this.",
        "Work upload, authorship radio button, Yes option text."),
    'WORK_AUTHORSHIP_NO': (
        "No, I don't own these rights, but I still want to upload this work, knowing that it might be"
        "transferred to another person or removed from the awards if there's a claim.",
        "Work upload, authorship radio button, No option text."),
    'WORK_AUTHORSHIP_MAYBE': (
        "I don't know if I'm allowed or not to enroll this work to the awards, but I still want to upload this "
        "work, knowing that it might be transferred to another person or removed from the awards if "
        "there's a claim.",
        "Work upload, authorship radio button, Maybe option text."),
}
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

FIXTURES_PATH_TO_COVERS = 'test-images/covers'
FIXTURES_PATH_TO_LITTLE = 'test-images/littles'
FIXTURES_PATH_TO_AVATARS = 'test-images/avatars'

# Storage Service

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = 'codi.coop.test'
AWS_S3_CUSTOM_DOMAIN = f's3.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}'
AWS_S3_ENDPOINT_URL = 'https://s3.wasabisys.com'
AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'apps.openawards.lib.storages.MediaStorage'
EXTERNAL_MEDIA_PATH = 'openawards/media'
MEDIA_FILE_OVERWRITE = True

EMAIL_SUBJECT_PREFIX = '[OpenAwards]'
