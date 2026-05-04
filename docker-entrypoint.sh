#!/bin/ash

echo "Apply database migrations"

# shared/public schema
python manage.py migrate_schemas --shared

# tenant schemas with multiprocessing executor
python manage.py migrate_schemas --executor=multiprocessing --noinput

echo "Starting server"
gunicorn --worker-class gevent --bind 0.0.0.0:80 --access-logfile - dashboard_service.wsgi & celery -A dashboard_service worker -l info -c 1
