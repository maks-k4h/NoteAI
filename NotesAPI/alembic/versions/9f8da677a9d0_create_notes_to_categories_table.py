"""create notes_to_categories table

Revision ID: 9f8da677a9d0
Revises: 14e01f4ee0b6
Create Date: 2023-09-01 17:37:59.454405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f8da677a9d0'
down_revision: Union[str, None] = '14e01f4ee0b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('notes_to_categories',
        sa.Column('note_uuid', sa.UUID(), nullable=False),
        sa.Column('category_uuid', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['category_uuid'], ['categories.uuid'], ),
        sa.ForeignKeyConstraint(['note_uuid'], ['notes.uuid'], ),
        sa.PrimaryKeyConstraint('note_uuid', 'category_uuid')
    )


def downgrade() -> None:
    op.drop_table('notes_to_categories')
