web: python manage.py migrate --noinput && gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 4
release: python manage.py migrate --noinput
