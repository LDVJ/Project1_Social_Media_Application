from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

DATABSAE_URL = 'postgresql+psycopg://postgres:ldvj1242210%40L@localhost/project1'

engine = create_engine(DATABSAE_URL)

sessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=engine)

Base = declarative_base()