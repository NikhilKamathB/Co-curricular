"""
Django settings for django_elasticsearch project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

'''
To use Jaejer, install docker and run:

docker run -d --name jaeger \                                                                                                                        tyche@tyche
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.29

To use postgres in docker:

docker run -d --name postgres -p 5499:5432 \
-e POSTGRES_USER=django_elasticsearch \
-e POSTGRES_PASSWORD=django_elasticsearch \
-e POSTGRES_DB=django_elasticsearch \
postgres:latest

'''

import os
from pathlib import Path
import django_opentracing
from jaeger_client import Config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d!w(kmv7)d@#q@nq%ht+3=$roz%isn$8*rjla$c+zc(h3=7fjh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'import_export',
    'rest_framework',
    'django_opentracing',

    # Custom apps
    'accounts.apps.AccountsConfig',
    'book.apps.BookConfig',
    'api.apps.ApiConfig'
]

MIDDLEWARE = [
    'django_opentracing.OpenTracingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'django_elasticsearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'django_elasticsearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': os.getenv("PGDATABASE", "django_elasticsearch"),
      'USER': os.getenv("PGUSER", "django_elasticsearch"),
      'PASSWORD': os.getenv("PGPASSWORD", "django_elasticsearch"),
      'HOST': os.getenv("PGHOST", "127.0.0.1"),
      'PORT': os.getenv("PGPORT", "5499"),
  },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom account.
AUTH_USER_MODEL = 'accounts.User'

# Open-tracing
OPENTRACING_TRACE_ALL = True
config = Config(
    config={ # usually read from some yaml config
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'local_agent': {
            'reporting_host': 'localhost',
            'reporting_port': '5775',
        },
        'logging': True,
    },
    service_name='python-django-elascticsearch',
    validate=True
)
# this call also sets opentracing.tracer
tracer = config.initialize_tracer()
OPENTRACING_TRACING = django_opentracing.DjangoTracing(tracer)