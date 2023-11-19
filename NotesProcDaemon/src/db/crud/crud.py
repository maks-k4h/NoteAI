import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Session
from ... import models

from .. import database


def init_message_tracker(session: Session, commit=True):
    num_records = session.query(sa.func.count(models.LastProcessedMessage.message_id)).scalar()

    if num_records > 1:
        raise Exception(f'Number of records in {models.LastProcessedMessage.__tablename__} > 1.')

    if num_records < 1:
        lpm = models.LastProcessedMessage()
        lpm.message_id = '0-0'
        session.add(lpm)
        if commit:
            session.commit()


def get_last_message_id(session: Session):
    return session.scalar(sa.select(models.LastProcessedMessage.message_id))


def set_last_message_id(session: Session, id: str, commit=True):
    session.execute(sa.update(models.LastProcessedMessage).values(message_id=id))
    if commit:
        session.commit()



