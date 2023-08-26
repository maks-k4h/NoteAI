"""create users_to_categories table

Revision ID: ce59f600242b
Revises: 24393f3d4ad3
Create Date: 2023-08-26 21:18:50.077212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce59f600242b'
down_revision: Union[str, None] = '24393f3d4ad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users_to_categories',
        sa.Column('user_uuid', sa.Uuid, primary_key=True),
        sa.Column('category_uuid', sa.Uuid, primary_key=True),
        sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid']),
        sa.ForeignKeyConstraint(['category_uuid'], ['categories.uuid'])
    )


def downgrade() -> None:
    op.drop_table('users_to_categories')
