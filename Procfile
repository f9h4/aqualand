web: gunicorn aqualand.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --worker-class sync --timeout 60 --chdir ./aqualand --log-level info
release: cd aqualand && python manage.py migrate --noinput && python manage.py collectstatic --noinput
