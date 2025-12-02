web: cd aqualand && gunicorn aqualand.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --access-logfile -
release: cd aqualand && python init_railway.py
