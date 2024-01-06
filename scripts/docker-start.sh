#!/bin/sh

set -e

./scripts/wait-for-postgres.sh $POSTGRES_HOST
poetry run alembic upgrade head



# Run SQL scripts
for script in ./scripts/seed/*.sql; do
    PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f $script
done

poetry run uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload