web: cd ./src/DRFProject python manage.py migrate --no-input
web: gunicorn --chdir ./src/DRFProject DRFProject.wsgi --log-file -