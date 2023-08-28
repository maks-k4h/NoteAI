"""Create notes table

Revision ID: 14e01f4ee0b6
Revises: 4ab2421d47c8
Create Date: 2023-08-28 18:32:48.416425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14e01f4ee0b6'
down_revision: Union[str, None] = '4ab2421d47c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notes',
        sa.Column('uuid', sa.Uuid(), primary_key=True),
        sa.Column('user_uuid', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=256), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ),
    )


def downgrade() -> None:
    op.drop_table('notes')
