import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine

# from sqlalchemy.ext.declarative import DeclarativeMeta,
from sqlalchemy.orm import sessionmaker

# Replace these values with your actual environment variable names
DB_HOST = os.environ["POSTGRES_HOST"]
DB_NAME = os.environ["POSTGRES_DATABASE"]
DB_USER = os.environ["POSTGRES_USERNAME"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]

# Construct the connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: DeclarativeMeta = declarative_base()
