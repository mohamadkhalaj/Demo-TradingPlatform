FROM python:latest

ENV DJANGO_SUPERUSER_PASSWORD admin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DEBUG 0
ENV REDIS_HOST redis
ENV DJANGO_SECRET_KEY "secretsecretsecretsecret123456"
ENV DJANGO_SETTINGS_MODULE "config.settings.production"
ENV DJANGO_ALLOWED_HOSTS "*"
ENV DJANGO_ADMIN_URL "admin/"
ENV EMAIL_HOST_USER ""
ENV EMAIL_HOST_PASSWORD ""
ENV SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ""
ENV SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET ""
ENV HCAPTCHA_SITEKEY ""
ENV HCAPTCHA_SECRET ""
ENV CRYPTO_COMPARE_API ""
ENV SENTRY_DSN ""
ENV REDIS_URL redis
ENV DATABASE_URL "postgres://postgres:postgres@db:5432/postgres"

RUN mkdir /web
RUN touch /web/requirements.txt
RUN echo "-r requirements/production.txt" >> /web/requirements.txt
COPY ./requirements /web/requirements

WORKDIR /web

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD while ! python manage.py sqlflush > /dev/null 2>&1; do sleep 1; done && \
	python manage.py makemigrations --noinput && \
	python manage.py migrate --noinput && \
	python manage.py migrate --run-syncdb --noinput && \
	python manage.py collectstatic --noinput && \
	python manage.py createsuperuser --user admin --email exchange@localhost --noinput > /dev/null; \
	daphne -b 0.0.0.0 -p 8000 config.routing:application