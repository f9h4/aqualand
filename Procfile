web: gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2 --chdir ./aqualand
release: cd aqualand && python manage.py migrate && python manage.py collectstatic --noinput
