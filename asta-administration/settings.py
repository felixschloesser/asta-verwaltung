"""
Django settings for keyManagement project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os, json, re
from os.path import join, dirname
from dotenv import load_dotenv

import logging


# Get secrets from .env file
load_dotenv()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'changeme')

HASHID_FIELD_SALT = os.getenv('DJANGO_HASHID_FIELD_SALT', 'changeme')

SIMPLE_HISTORY_REVERT_DISABLED=True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', True)


ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS','localhost').split(' ')
#ALLOWED_HOSTS = ['10.0.0.25', '134.28.72.225', 'localhost', '31.18.186.22']

INTERNAL_IPS = [
    '127.0.0.1',
]


IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$')
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
    ,

    # 3rd party
    'mozilla_django_oidc', # Enable Open ID Connect Login though gitlab
    'rest_framework',
    'django_extensions',
    'widget_tweaks',
    'phonenumber_field',
    'simple_history',
    'debug_toolbar',
    'fontawesome-free',

    # Local
    'keys',
   #'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # serve static files without nginx
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
]

ROOT_URLCONF = 'asta-administration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'asta-administration.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(
             os.getenv('DJANGO_DB_ENGINE', 'postgresql_psycopg2')
        ),
        'NAME': os.getenv('DB_NAME', 'astadb'),
        'USER': os.getenv('DB_USER', 'django'),
        'PASSWORD': os.getenv('DB_PASSWORD','changeme'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', ''),
        'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', '0')),
        'OPTIONS': json.loads(
             os.getenv('DJANGO_DB_OPTIONS', '{}')
        ),
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

#Gitlab Open ID SigleSingOn (SSO)

#Add 'mozilla_django_oidc' authentication backend



AUTHENTICATION_BACKENDS = ['asta-administration.auth.CustomOpenidBackend']

OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET')

OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_JWKS_ENDPOINT = "https://collaborating.tuhh.de/oauth/discovery/keys"

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://collaborating.tuhh.de/oauth/authorize"
OIDC_OP_TOKEN_ENDPOINT = "https://collaborating.tuhh.de/oauth/token"
OIDC_OP_USER_ENDPOINT = "https://collaborating.tuhh.de/oauth/userinfo"
OIDC_RP_SCOPES = "openid profile email"

LOGIN_REDIRECT_URL = "https://verwaltung.asta.felixschloesser.de/keys/"
LOGIN_REDIRECT_URL_FAILURE = "https://verwaltung.asta.felixschloesser.de/keys/"
LOGOUT_REDIRECT_URL = "https://verwaltung.asta.felixschloesser.de/keys/"
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'de-DE'

PHONENUMBER_DEFAULT_REGION = 'DE'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'

TIME_ZONE = 'Europe/Berlin'

USE_TZ = True
USE_L10N = True

# Mail
EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('DJANGO_EMAIL_USE_TLS')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

WHITENOISE_ROOT = os.path.join(STATIC_ROOT, 'root')
STATICFILES_STORAGE = os.getenv('DJANGO_STATICFILES_STORAGE')

# Logging Configuration

# Clear prev config
#LOGGING_CONFIG = None
#LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'debug').upper()

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG',
    },
}
