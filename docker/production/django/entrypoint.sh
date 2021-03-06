#!/usr/bin/env bash

set -o errexit
set -o pipefail

# todo: turn on after #1295
# set -o nounset


cmd="$@"

# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.

if [ -z "$REDIS_URL" ]; then
    export REDIS_URL=redis://redis:6379
fi

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi

if [ -z "$POSTGRES_HOST" ]; then
        export POSTGRES_HOST=postgis
fi

export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_USER
export CELERY_BROKER_URL=$REDIS_URL/0


function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_USER", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
counter=1
until postgres_ready; do
  if [ "${counter}" -eq "1" ]; then
    >&2 echo "Postgres is unavailable - sleeping"
  fi
  counter=$((counter +1))
  sleep 1
done

>&2 echo "Postgres is up - continuing..."
exec $cmd
