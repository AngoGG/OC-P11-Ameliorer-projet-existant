release: python manage.py migrate && python manage.py fill_database

web: gunicorn purbeurre.wsgi --log-file -