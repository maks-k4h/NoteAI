import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db.database import Base
from pgvector.sqlalchemy import Vector


class LastProcessedMessage(Base):
    __tablename__ = 'last_processed_message'

    message_id: Mapped[str] = mapped_column(primary_key=True, nullable=False, default='0-0')

    def __repr__(self) -> str:
        return f'LastProcessedMessage(message_id={self.message_id})'


class NoteCategoryEmbedding(Base):
    __tablename__ = 'note_category_embeddings'

    uuid = mapped_column(sa.Uuid, primary_key=True)
    note_category_uuid = mapped_column(sa.Uuid, nullable=False)
    version: Mapped[str] = mapped_column(sa.String, nullable=False)
    embedding_768 = mapped_column(Vector(768))


class NoteEmbedding(Base):
    __tablename__ = 'note_embedding'

    uuid = mapped_column(sa.Uuid, primary_key=True)
    note_uuid = mapped_column(sa.Uuid, nullable=False)
    version: Mapped[str] = mapped_column(sa.String, nullable=False)
    embedding_768 = mapped_column(Vector(768))

