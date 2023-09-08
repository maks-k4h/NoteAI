"""create message tracking table

Revision ID: 9133548469e2
Revises: 
Create Date: 2023-09-08 18:32:28.056489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9133548469e2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('last_processed_message',
    sa.Column('message_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('message_id')
    )


def downgrade() -> None:
    op.drop_table('last_processed_message')
