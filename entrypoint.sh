#!/bin/bash
cd app
python manage.py wait_for_postgres
python manage.py makemigrations
python manage.py migrate
uvicorn medway_api.asgi:application --host 0.0.0.0 --port 8000 --reload