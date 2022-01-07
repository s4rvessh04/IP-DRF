release: cd ./src/DRFProject python manage.py migrate --no-input

web: gunicorn DRFProject.wsgi --log-file -