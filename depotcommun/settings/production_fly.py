from .base import *
import os
import dj_database_url

DATABASES = {
    'default' : dj_database_url.config()
}

APP_NAME = os.environ.get("FLY_APP_NAME")
ALLOWED_HOSTS = [f"{APP_NAME}.fly.dev"] 

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

