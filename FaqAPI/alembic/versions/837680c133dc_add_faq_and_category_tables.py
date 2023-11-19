"""add faq and category tables

Revision ID: 837680c133dc
Revises: 
Create Date: 2023-11-19 14:47:36.700791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '837680c133dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('faq_categories',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('faq',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('category_uuid', sa.Uuid(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['category_uuid'], ['faq_categories.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    op.drop_table('faq')
    op.drop_table('faq_categories')
