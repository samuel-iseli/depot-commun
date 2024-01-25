from .base import *
import os
import dj_database_url

DATABASES = {
    'default' : dj_database_url.config()
}

APP_NAME = os.environ.get("FLY_APP_NAME")
ALLOWED_HOSTS = [f"{APP_NAME}.fly.dev"] 
CSRF_TRUSTED_ORIGINS = [f"https://{APP_NAME}.fly.dev"]

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

