FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST redis
ENV DJANGO_SETTINGS_MODULE "config.settings.production"
ENV REDIS_URL redis
ENV DJANGO_ALLOWED_HOSTS "*"
ENV DATABASE_URL "postgres://postgres:postgres@db:5432/postgres"

RUN mkdir /web
RUN touch /web/requirements.txt
RUN echo "-r requirements/production.txt" >> /web/requirements.txt
COPY ./requirements /web/requirements

WORKDIR /web

RUN pip install --upgrade pip
RUN pip install -r requirements.txt