
import sqlalchemy as sa
from sqlalchemy import orm

from ... import models


# CREATE

def put_note(session: orm.Session, note: models.Note) -> bool:
    try:
        session.add(note)
        session.commit()
        return True
    except:
        return False


# READ

def get_by_uuid(session: orm.Session, uuid: sa.UUID):
    return session.get(models.Note, uuid)


def get_by_user_uuid(session: orm.Session, user_uuid: sa.UUID, offset=0, limit: int | None = None):
    stmt = sa.select(models.Note).where(models.Note.user_uuid == user_uuid).offset(offset).limit(limit)
    result = session.execute(stmt).scalars()
    notes = result.all()
    return notes


# UPDATE


# DELETE

def delete(session: orm.Session, note: models.Note) -> bool:
    try:
        session.delete(note)
        session.commit()
        return True
    except:
        return False

