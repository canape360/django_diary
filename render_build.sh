#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt
find staticfiles -type f -delete 2>/dev/null || true
python manage.py collectstatic --noinput --clear
python manage.py migrate
