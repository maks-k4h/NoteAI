import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from dotenv import find_dotenv, load_dotenv


# load env variables
load_dotenv(find_dotenv())

DATABASE_URL = os.getenv('DATABASE_URL')


engine = create_engine(DATABASE_URL, echo=False, )


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=True,
)


class Base(DeclarativeBase):
    pass

