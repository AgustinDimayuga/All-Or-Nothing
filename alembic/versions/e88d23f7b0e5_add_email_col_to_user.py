"""Add email col to user

Revision ID: e88d23f7b0e5
Revises: 9d8d7fdd16e4
Create Date: 2026-05-01 11:08:14.587762

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e88d23f7b0e5"
down_revision: Union[str, Sequence[str], None] = "9d8d7fdd16e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("email", sa.String, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "email")
    pass
