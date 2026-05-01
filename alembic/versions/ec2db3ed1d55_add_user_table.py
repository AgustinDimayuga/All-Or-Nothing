"""Add user table

Revision ID: ec2db3ed1d55
Revises:
Create Date: 2026-05-01 10:44:50.814289

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ec2db3ed1d55"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users", sa.Column("id", sa.Integer, primary_key=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
