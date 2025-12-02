release: cd aqualand && python init_railway.py
web: cd aqualand && gunicorn aqualand.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --worker-class sync --timeout 120 --access-logfile - --error-logfile - --log-level debug
