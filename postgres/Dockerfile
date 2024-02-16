FROM postgis/postgis:14-3.4


# Enable the uuid-ossp extension in PostgreSQL
RUN echo "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";" > /docker-entrypoint-initdb.d/uuid-ossp.sql
