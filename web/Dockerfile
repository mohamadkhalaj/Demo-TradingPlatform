FROM python:latest

ENV DJANGO_SUPERUSER_PASSWORD admin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DEBUG False
ENV REDIS_HOST redis

RUN mkdir /web
COPY ./requirements.txt /web/requirements.txt

WORKDIR /web

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py makemigrations --noinput && \
	python manage.py migrate --noinput && \
	python manage.py migrate --run-syncdb --noinput && \
	python manage.py collectstatic --noinput && \
	python manage.py createsuperuser --user admin --email exchange@localhost --noinput > /dev/null; \
	daphne -b 0.0.0.0 -p 8000 config.routing:application