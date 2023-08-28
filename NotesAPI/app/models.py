from __future__ import annotations

from .db.database import Base

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, relationship, Mapped

# Database Models Definitions


users_to_categories_association_table = sa.Table(
    'users_to_categories',
    Base.metadata,
    sa.Column('user_uuid', sa.UUID, primary_key=True),
    sa.Column('category_uuid', sa.UUID, primary_key=True),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid']),
    sa.ForeignKeyConstraint(['category_uuid'], ['categories.uuid'])
)


class User(Base):
    __tablename__ = 'users'

    uuid = mapped_column(sa.Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(64), nullable=False)
    password: Mapped[str] = mapped_column(sa.String(64), nullable=False)

    user_meta: Mapped[UserMeta] = relationship(back_populates='user')
    categories: Mapped[list[Category]] = relationship(secondary=users_to_categories_association_table, back_populates='users')
    notes: Mapped[list[Note]] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f'User(uuid={self.uuid}, email={self.email}, password={self.password})'


class Category(Base):
    __tablename__ = 'categories'

    uuid = mapped_column(sa.Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(128), nullable=False, unique=True)

    users: Mapped[list[User]] = relationship(secondary=users_to_categories_association_table, back_populates='categories')

    def __repr__(self) -> str:
        return f'Category(uuid={self.uuid}, name={self.name})'


class UserMeta(Base):
    __tablename__ = 'users_meta'

    user_uuid = mapped_column(sa.ForeignKey('users.uuid'), primary_key=True)
    email: Mapped[str] = mapped_column(sa.String(321), nullable=False)

    user: Mapped[User] = relationship(back_populates='user_meta')

    def __repr__(self) -> str:
        return f'UserMeta(user_uuid={self.user_uuid}, email={self.name})'


class Note(Base):
    __tablename__ = 'notes'

    uuid = mapped_column(sa.Uuid, primary_key=True)
    user_uuid = mapped_column(sa.ForeignKey('users.uuid'), nullable=False)
    title: Mapped[str] = mapped_column(sa.String(256), nullable=True)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)

    user: Mapped[User] = relationship(back_populates='notes')

    def __repr__(self):
        return (f'Note(uuid={self.uuid.__str__()}, '
                f'user_uuid={self.user_uuid.__str__()}, '
                f'title="{self.title}, '
                f'content={self.content[:30] + "..." if len(self.content) > 30 else self.content}")')

