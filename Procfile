release: ./react-build.sh
release: python manage.py migrate --settings=depotcommun.settings.production
web: gunicorn depotcommun.wsgi
