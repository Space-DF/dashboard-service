#!/bin/ash

echo "Apply database migrations"
python manage.py migrate_smart || exit 1

echo "Starting downgrade consumer"
python manage.py run_downgrade_dashboard_consumer &

echo "Starting server"
gunicorn --worker-class gevent --bind 0.0.0.0:80 --access-logfile - dashboard_service.wsgi & celery -A dashboard_service worker -l info -c 1
