release: python manage.py migrate --settings=depotcommun.settings.production
release: ./react-build.sh
web: gunicorn depotcommun.wsgi
