import sqlalchemy as sa
from sqlalchemy.orm import Session

from ... import models


# INSERT
def add_note_embedding(session: Session, note_embedding: models.NoteEmbedding):
    try:
        session.add(note_embedding)
        session.commit()
        return True
    except:
        return False


def add_note_category_embedding(session: Session, note_category_embedding: models.NoteCategoryEmbedding):
    try:
        session.add(note_category_embedding)
        session.commit()
        return True
    except:
        return False


# GET
def get_note_embedding_by_note(session: Session, note_uuid: str):
    q = sa.select(models.NoteEmbedding).where(models.NoteEmbedding.note_uuid == note_uuid)
    res = session.execute(q)
    return res.scalar_one_or_none()


def get_knn_categories(session: Session, note_emb, user_uuid: str, n=1) -> list[str]:
    q = sa.text(f'SELECT E.note_category_uuid '
                f'FROM {models.NoteCategoryEmbedding.__tablename__} E '
                f'ORDER BY E.embedding_768 <-> \'{list(note_emb)}\' '
                f'LIMIT {n};')
    res = session.execute(q)
    return [str(u) for u in res.scalars().all()]
