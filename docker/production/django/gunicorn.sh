#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python /app/radon/manage.py migrate
python /app/radon/manage.py collectstatic --noinput
python /app/radon/manage.py createsu
python /app/radon/manage.py importshape
gunicorn radon.config.wsgi -w 4 -b 0.0.0.0:8000 -t 80 --graceful-timeout 80 --chdir=/app/radon
