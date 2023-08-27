
import sqlalchemy as sa
from sqlalchemy import orm
from ..database import sessionmaker
from ... import models

from uuid import UUID


# CREATE
def put_user(session: orm.Session, user: models.User) -> bool:
    try:
        session.add(user)
        session.commit()
        return True
    except:
        return False


# READ
def get_by_uuid(session: orm.Session, uuid: UUID):
    return session.get(models.User, uuid)


def get_by_name(session: orm.Session, name: str):
    return session.scalar(sa.select(models.User).filter(models.User.name == name))


def check_name(session: orm.Session, name: str) -> bool:
    return session.query(session.query(models.User).filter(models.User.name == name).exists()).scalar()


def check_email(session: orm.Session, email: str) -> bool:
    return session.query(session.query(models.UserMeta).filter(models.UserMeta.email == email).exists()).scalar()