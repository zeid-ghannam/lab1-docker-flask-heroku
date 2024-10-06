#!/bin/sh

# if local
until pg_isready -h db -U admin -d distlab; do
# if remote
# until pg_isready -h dpg-cs0il423esus739369m0-a.frankfurt-postgres.render.com -U persona_id_user -d persona_id; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready!"

python init_db.py

# flask db init
# flask db upgrade

exec gunicorn --config config.py run:app