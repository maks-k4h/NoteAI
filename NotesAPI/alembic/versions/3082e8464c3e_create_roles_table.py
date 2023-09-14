"""create roles table

Revision ID: 3082e8464c3e
Revises: 9f8da677a9d0
Create Date: 2023-09-15 00:22:50.759311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3082e8464c3e'
down_revision: Union[str, None] = '9f8da677a9d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('uuid', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )
    op.add_column('users', sa.Column('role_uuid', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_uuid'], ['uuid'])


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_uuid')
    op.drop_table('roles')
