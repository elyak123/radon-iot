#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python /app/radon/manage.py migrate
python /app/radon/manage.py collectstatic --noinput
gunicorn radon.config.wsgi -w 4 -b 0.0.0.0:5000 -t 80 --graceful-timeout 80 --chdir=/app/radon
