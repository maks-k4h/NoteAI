"""add tables for category embeddings

Revision ID: d574c05dd4c4
Revises: 9133548469e2
Create Date: 2023-10-29 12:28:21.420538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'd574c05dd4c4'
down_revision: Union[str, None] = '9133548469e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('note_category_embeddings',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('note_category_uuid', sa.Uuid(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('embedding_768', pgvector.sqlalchemy.Vector(dim=768), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('note_embedding',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('note_uuid', sa.Uuid(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('embedding_768', pgvector.sqlalchemy.Vector(dim=768), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    op.drop_table('note_embedding')
    op.drop_table('note_category_embeddings')
