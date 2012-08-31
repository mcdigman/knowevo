web: bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT knowevo/settings.py
worker: bin/python knowevo/manage.py celeryd -E -B --loglevel=INFO