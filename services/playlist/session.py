import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

host = os.getenv('PQ_HOST', "postgres-db-postgresql")
port = os.getenv('PQ_PORT', 5432)
user = os.getenv('PQ_USER', "root")
passWd = os.getenv('PQ_PASS', "algo123")
pqdb = os.getenv('PQ_DB', "spotifyre_db")

url = URL.create(
    drivername="postgresql+psycopg2",
    username=user,
    password=passWd,
    host=host,
    port=port,
    database=pqdb
)

engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()
