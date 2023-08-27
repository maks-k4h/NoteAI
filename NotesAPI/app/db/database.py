import os

from .. import DEBUG

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = os.getenv('DATABASE_URL')


engine = create_engine(DATABASE_URL, echo=DEBUG, )


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db_session():
    """FastAPI dependency for acquiring database session."""
    with SessionLocal() as session:
        yield session



class Base(DeclarativeBase):
    pass

