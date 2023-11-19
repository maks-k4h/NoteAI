"""create images table

Revision ID: cd93861a05dd
Revises: 3082e8464c3e
Create Date: 2023-11-19 18:13:08.802564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd93861a05dd'
down_revision: Union[str, None] = '3082e8464c3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('images',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('user_uuid', sa.Uuid(), nullable=False),
    sa.Column('added', sa.DateTime(), nullable=False),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    op.drop_table('images')
