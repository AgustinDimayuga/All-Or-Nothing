"""add idempotency tables

Revision ID: 4a4c3e3e5379
Revises: 383d64614811
Create Date: 2026-05-11 13:14:13.831598

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4a4c3e3e5379"
down_revision: Union[str, Sequence[str], None] = "383d64614811"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "processed_bets",
        sa.Column("key", sa.String, primary_key=True),
        sa.Column("response", sa.JSON, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("processed_bets")
