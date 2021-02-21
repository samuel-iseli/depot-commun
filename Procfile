release: ./react-build.sh
release: python manage.py migrate --settings=depotcommun.settings.production
release: python manage.py collectstatic --noinput
web: gunicorn depotcommun.wsgi
