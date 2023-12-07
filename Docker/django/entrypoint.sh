#!/bin/sh

set -e

#until pg_isready -h postgres -p 5432 -U postgres; do
#    echo "Waiting for PostgreSQL to become ready..."
#    sleep 2
#done

echo "Applying database migrations..."
python manage.py migrate

# Load data from django_app/fixtures
echo "Loading data from fixtures..."
echo "Loading categories..."
python manage.py loaddata django_app/fixtures/categories.json

python manage.py runserver 0.0.0.0:8000
