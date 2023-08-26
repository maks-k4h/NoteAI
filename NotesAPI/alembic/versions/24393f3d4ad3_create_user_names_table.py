"""create user_names table

Revision ID: 24393f3d4ad3
Revises: f265dc2d4c48
Create Date: 2023-08-26 21:04:09.460325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24393f3d4ad3'
down_revision: Union[str, None] = 'f265dc2d4c48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # keeping users' names in separate relation to maintain 3NF
    op.create_table(
        'user_names',
        sa.Column('user_uuid', sa.Uuid, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'])
    )


def downgrade() -> None:
    op.drop_table('user_names')
