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

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'depotcommun.settings.production')

# add parentdir of depotcommun to path to allow import of depotcommun
parentdir = str(pathlib.Path(__file__).parent.parent)
sys.path.append(parentdir)

_application = get_wsgi_application()
env_vars_to_pass = ['DJANGO_SECRET_KEY', 'DJANGO_SETTINGS_MODULE', 'EMAIL_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_USER', 'POSTGRES_PASSWORD']


def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_vars_to_pass:
        value = environ.get(var, '')
        if value:
            os.environ[var] = value

    return _application(environ, start_response)