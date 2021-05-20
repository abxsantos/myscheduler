#!/bin/bash
python manage.py makemigrations

python manage.py migrate

python manage.py runserver "$DJANGO_DEV_HOST":"$DJANGO_DEV_PORT"