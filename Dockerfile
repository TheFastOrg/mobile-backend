FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry install --no-root

COPY ./src /app/src

RUN apt-get update && apt-get install -y postgresql-client

COPY wait-for-postgres.sh /wait-for-postgres.sh

RUN chmod +x /wait-for-postgres.sh

ENTRYPOINT ["/wait-for-postgres.sh", "postgres", "poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
