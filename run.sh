#!/bin/bash

until nc -z "${DATABASE_HOST}" "${DATABASE_PORT}"; do
    echo "$(date) - waiting for postgres..."
    sleep 1
done

until nc -z "${REDIS_HOST}" "${REDIS_PORT}"; do
    echo "$(date) - waiting for redis..."
    sleep 1
done


celery -A "${PROJECT_NAME}" worker -l INFO
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py runserver "${GATEWAY_HOST}":"${GATEWAY_PORT}"
