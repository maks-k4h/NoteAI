"""create user tables

Revision ID: f265dc2d4c48
Revises: 469219bded99
Create Date: 2023-08-26 20:49:10.767661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f265dc2d4c48'
down_revision: Union[str, None] = '469219bded99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('uuid', sa.Uuid, primary_key=True),
        sa.Column('email', sa.String(321), nullable=False),     # assuming max len of 320
        sa.Column('password', sa.String(64), nullable=False)      # assuming hash len of 60
    )


def downgrade() -> None:
    op.drop_table('users')
