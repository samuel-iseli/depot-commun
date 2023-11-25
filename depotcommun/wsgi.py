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
parentdir = str(pathlib.Path(__file__).parent)
logging.error("added %s to sys.path" % parentdir)
sys.path.append(parentdir)

application = get_wsgi_application()
