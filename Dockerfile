FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock  /app/

RUN pip install poetry && poetry install --no-root

RUN apt-get update && apt-get install -y postgresql-client

COPY ./src /app/src

COPY scripts/ /app/scripts/

COPY alembic.ini poetry.lock  /app/

COPY tests/  /app/tests/

RUN chmod -R +x /app/scripts/

ENTRYPOINT ["/app/scripts/docker-start.sh"]
