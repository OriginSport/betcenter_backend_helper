#coding=utf-8
"""
Django settings for ttraffle project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qzx@7axm^$go-3147gyc-qekku(w*nh*^00182$@633^=+yh#9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DB_ECHO = True
TEST_ECHO = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'daterange_filter',
    'corsheaders',
    'betcenter_backend_helper.bet',
    'betcenter_backend_helper.bet_record',
    'betcenter_backend_helper.bet_detail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'betcenter_backend_helper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'betcenter_backend_helper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


APPID = 'crushsport'
PLATFORM = 30

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/')
MEDIA_URL = '/upload/'

LOG_LEVEL = "debug"

HOST = "0.0.0.0"
PORT = 7040

DEFAULT_PAGE_CACHE_TIMEOUT = 60  * 5

DEFAULT_RANDOM_USER_COUNT = 10

DEFAULT_RAFFLE_LIST_CACHE_TIMEOUT = 60  * 60

# DEFAULT_RANK_LIST_LIMIT
DEFAULT_CRIT_RATE_RANK_LIST_LIMIT = 10
DEFAULT_WIN_TIMES_RANK_LIST_LIMIT = 10

# DEFAULT_PAGE_SIZE
APP_PAGINATOR_DEFAULT_PAGE_SIZE = 10
APP_PAGINATOR_DEFAULT_WIDTH =  10
APP_PAGINATOR_DEFAULT_LMARGIN = 3

CORS_ORIGIN_ALLOW_ALL = True

# Memcache
MEMCACHED_CACHE_SERVERS = ['127.0.0.1:11211',]

# Redis
COUNTER_REDIS_SERVER = '127.0.0.1'
COUNTER_REDIS_PORT = 6379
COUNTER_REDIS_PAS = ''

DB_USERPACK_SHARD_MOD = 100

MYSQL_DB_POOL_SIZE = 100
MYSQL_DB_POOL_RECYCLE_TIMEOUT = 60 * 60 * 2

DIRECT_MSG_MESSAGE_CHANNEL = 'PAY'

# Newbie
NEWBIE_COMPETITOR_ID = 15

from .site_settings import *


