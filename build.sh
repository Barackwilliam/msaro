#!/usr/bin/env bash
# Render build command:  ./build.sh
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
# Loads the website content the first time (fills empty tables only, never
# overwrites anything edited in the admin).
python manage.py seed_site
