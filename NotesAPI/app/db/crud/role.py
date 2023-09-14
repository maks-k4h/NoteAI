import sqlalchemy as sa
from sqlalchemy import orm
from ... import models

from uuid import UUID


# CREATE
def put(session: orm.Session, role: models.Role) -> bool:
    try:
        session.add(role)
        session.commit()
        return True
    except:
        return False


# READ
def get_by_uuid(session: orm.Session, uuid: UUID):
    return session.get(models.Role, uuid)


def get_by_name(session: orm.Session, name: str):
    return session.scalar(sa.select(models.Role).filter(models.Role.name == name))

