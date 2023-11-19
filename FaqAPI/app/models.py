from __future__ import annotations

from .db.database import Base

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, relationship, Mapped

# Database Models Definitions


class Faq(Base):
    __tablename__ = 'faq'

    uuid = mapped_column(sa.Uuid, primary_key=True)
    category_uuid = mapped_column(sa.ForeignKey('faq_categories.uuid'), nullable='False')
    question = mapped_column(sa.String(), nullable=False)
    answer = mapped_column(sa.String(), nullable=False)

    category: Mapped[FaqCategory] = relationship(back_populates='faqs')

    def __repr__(self) -> str:
        return (f'Faq(uuid={self.uuid}, category_uuid={self.category_uuid}, '
                f'question={self.question[:20] + "..." if len(self.question) >= 20 else self.question}, '
                f'answer={self.answer[:20] + "..." if len(self.answer) >= 20 else self.answer})')


class FaqCategory(Base):
    __tablename__ = 'faq_categories'

    uuid = mapped_column(sa.Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(), nullable=False)
    description: Mapped[str] = mapped_column(sa.String(), nullable=True)

    faqs: Mapped[list[Faq]] = relationship(back_populates='category')

    def __repr__(self) -> str:
        return (f'FaqCategory(uuid={self.uuid}, '
                f'name={self.name[:20] + "..." if len(self.name) >= 20 else self.name}, '
                f'description={self.description[:20] + "..." if len(self.description) >= 20 else self.description})')

