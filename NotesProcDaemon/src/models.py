import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db.database import Base


class LastProcessedMessage(Base):
    __tablename__ = 'last_processed_message'

    message_id: Mapped[str] = mapped_column(primary_key=True, nullable=False, default='0-0')

    def __repr__(self) -> str:
        return f'LastProcessedMessage(message_id={self.message_id})'
