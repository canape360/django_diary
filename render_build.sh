#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# スーパーユーザーが未作成なら作成
python manage.py createsuperuser --noinput || true
