from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import  declarative_base
from .config import settings


DATABSAE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOSTNAME,
    port=settings.DB_PORT,
    database=settings.DB_NAME
)
engine = create_engine(DATABSAE_URL)

sessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionLocal()
    try:
        print("DB connected Successfully")
        yield db
    finally:
        print('DB Disconnected')
        db.close()