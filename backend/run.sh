#!/bin/sh
set -e

RETRIES=5

until psql -h $PGHOST -U $PGUSER -d $PGDATABASE -p $PGPORT -c "select 1" > /dev/null 2>&1  || [ $RETRIES -eq 0 ]; do
  echo "Login $PGHOST $PGUSER $PGDATABASE"
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 5
done

fastapi run /opt/backend/app/main.py --port 80