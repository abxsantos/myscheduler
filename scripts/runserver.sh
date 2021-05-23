#!/bin/bash

python manage.py makemigrations

python manage.py migrate

python manage.py seed_db --create-super-user

python manage.py runserver "$DJANGO_DEV_HOST":"$DJANGO_DEV_PORT"
