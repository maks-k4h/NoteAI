"""create categories table

Revision ID: 469219bded99
Revises: 
Create Date: 2023-08-26 19:59:07.497642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '469219bded99'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('uuid', sa.Uuid, primary_key=True),
        sa.Column('name', sa.VARCHAR(128), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table('categories')
