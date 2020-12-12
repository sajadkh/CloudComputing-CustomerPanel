#!/bin/bash

echo "start customer service...."
echo "create database..."
python initializer.py
echo "django makemigrations..."
python manage.py makemigrations appCustomer
echo "django migrate..."
python manage.py migrate
echo "run server..."
python manage.py runserver 0.0.0.0:8002
