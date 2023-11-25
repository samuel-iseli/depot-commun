"""
WSGI config for depotcommun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
import pathlib
import logging
import json

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'depotcommun.settings.production')

# add parentdir of depotcommun to path to allow import of depotcommun
path = pathlib.Path(__file__)
currentdir = str(path.parent)
parentdir = str(path.parent.parent)
sys.path.append(parentdir)

env_vars_to_pass = ['DJANGO_SECRET_KEY', 'DJANGO_SETTINGS_MODULE', 'EMAIL_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_USER', 'POSTGRES_PASSWORD']


def write_env():
    # write env variables to file to be able to load it in wsgi application
    env_dict = {}
    for var in env_vars_to_pass:
        env_dict[var] = os.environ.get(var, '')

    with open(os.path.join(currentdir, 'wsgienv'), 'w') as f:
        json.dump(env_dict, f)


def load_env():
    # load env variables from file
    with open(os.path.join(currentdir, 'wsgienv'), 'r') as f:
        env_dict = json.load(f)

    for var in env_vars_to_pass:
        value = env_dict.get(var, '')
        if value:
            os.environ[var] = value


def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    load_env()
    _application = get_wsgi_application()
    return _application(environ, start_response)
