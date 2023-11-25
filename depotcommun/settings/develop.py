from .base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # sqlite database
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'depotcommun.db',
        # postgres database
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'depot-commun',
        # 'USER': 'depot',
        # 'PASSWORD': 'KwCwHhW8q8RLzBT2VtJe',
    }
}

CORS_ALLOW_CREDENTIALS = True

# redirect to react debug server after login
# LOGIN_REDIRECT_URL = 'http://localhost:3000/'

# e-mail test backend with files
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'mail-output')

# logging
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
        'level': 'WARNING',
    }
}