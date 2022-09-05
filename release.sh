#!/bin/bash

python web/manage.py makemigrations && \
python web/manage.py migrate