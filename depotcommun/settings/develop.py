from .base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # sqlite database
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': 'depotcommun.db',
        # postgres database
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'depot-commun',
        'USER': 'postgres',
        'PASSWORD': 'password',
    }
}
