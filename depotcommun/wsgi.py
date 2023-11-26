"""
WSGI config for depotcommun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
import pathlib
import json

from django.core.wsgi import get_wsgi_application

# add parentdir of depotcommun to path to allow import of depotcommun
path = pathlib.Path(__file__)
currentdir = str(path.parent)
parentdir = str(path.parent.parent)
sys.path.append(parentdir)

env_vars_to_pass = ['DJANGO_SECRET_KEY', 'DJANGO_SETTINGS_MODULE', 'DJANGO_ALLOWED_HOSTS', 'EMAIL_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_USER', 'POSTGRES_PASSWORD']


def write_env():
    # write env variables to file to be able to load it in wsgi application
    env_dict = {}
    for var in env_vars_to_pass:
        env_dict[var] = os.environ.get(var, '')

    filepath = os.path.join(currentdir, 'wsgienv')
    with open(filepath, 'w') as f:
        json.dump(env_dict, f)


def load_env():
    # load env variables from file
    with open(os.path.join(currentdir, 'wsgienv'), 'r') as f:
        env_dict = json.load(f)

    for var in env_vars_to_pass:
        value = env_dict.get(var, '')
        if value:
            os.environ[var] = value


_application = None


def application(environ, start_response):
    # get application function, cache it if already present
    global _application
    if not _application:
        # load env variables from wsgienv file if present
        try:
            load_env()
        except Exception:
            pass
        _application = get_wsgi_application()

    return _application(environ, start_response)
