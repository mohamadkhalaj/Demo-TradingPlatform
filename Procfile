release: python web/manage.py migrate
web: cd web && daphne -b 0.0.0.0 -p $PORT config.routing:application