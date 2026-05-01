"""Add user cols

Revision ID: 9d8d7fdd16e4
Revises: ec2db3ed1d55
Create Date: 2026-05-01 10:59:52.819427

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9d8d7fdd16e4"
down_revision: Union[str, Sequence[str], None] = "ec2db3ed1d55"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("name", sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "name")
    pass
