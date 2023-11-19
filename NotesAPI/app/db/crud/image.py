import sqlalchemy as sa
from sqlalchemy import orm

from ... import models


# CREATE


# READ

def get_by_uuid(session: orm.Session, uuid: sa.UUID):
    return session.get(models.Image, uuid)


def get_images_by_user_uuid(session: orm.Session, user_uuid: sa.UUID, ignore_deleted=True):
    q = sa.select(models.Image).where(models.Image.user_uuid == user_uuid)
    if ignore_deleted:
        q = q.where(models.Image.deleted == None)

    res = session.execute(q)
    return res.scalars().all()


def get_deleted_images_by_user_uuid(session: orm.Session, user_uuid: sa.UUID):
    q = sa.select(models.Image).where(models.Image.user_uuid == user_uuid).where(models.Image.deleted != None)
    res = session.execute(q)
    return res.scalars().all()


# UPDATE


# DELETE

def delete(session: orm.Session, note: models.Note) -> bool:
    try:
        session.delete(note)
        session.commit()
        return True
    except:
        return False

