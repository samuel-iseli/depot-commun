from .base import *
import os

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'depot-commun',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# make sure http request are redirected to https
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# EMAIL password from heroku settings
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']

import django_heroku
django_heroku.settings(locals())