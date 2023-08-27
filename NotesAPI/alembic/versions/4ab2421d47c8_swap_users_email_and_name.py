"""swap users email and name

Revision ID: 4ab2421d47c8
Revises: ce59f600242b
Create Date: 2023-08-27 20:06:54.067230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ab2421d47c8'
down_revision: Union[str, None] = 'ce59f600242b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'email')
    op.drop_column('users_meta', 'name')

    op.add_column('users', sa.Column('name', sa.String(length=64), nullable=False))
    op.add_column('users_meta', sa.Column('email', sa.String(length=321), nullable=False))


def downgrade() -> None:
    op.drop_column('users_meta', 'email')
    op.drop_column('users', 'name')

    op.add_column('users_meta', sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('email', sa.VARCHAR(length=321), autoincrement=False, nullable=False))
