#!/usr/bin/env bash
# Script de build automatisé pour déploiement gratuit sur Render.com
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations accounts catalogue formations core --no-input
python manage.py migrate --no-input
python manage.py init_gabon_data || true
