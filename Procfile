release: chmod u+x release.sh && ./release.sh
web: cd web && daphne -b 0.0.0.0 -p $PORT config.routing:application
celery: cd web && python3 -m celery -A config worker -l info -c 4