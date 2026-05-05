"""add odds

Revision ID: 1e23635aa2fa
Revises: 4b2d0a27c69a
Create Date: 2026-05-04 20:14:29.768906

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1e23635aa2fa"
down_revision: Union[str, Sequence[str], None] = "4b2d0a27c69a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("bets", "odds")

    op.add_column("games", sa.Column("home_odds", sa.Float, nullable=False))
    op.add_column("games", sa.Column("away_odds", sa.Float, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column("bets", sa.Column("odds", sa.Float, nullable=False))

    op.drop_column("games", "home_odds")
    op.drop_column("games", "away_odds")
