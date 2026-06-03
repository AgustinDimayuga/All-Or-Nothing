"""add games indexes

Revision ID: ee3263825627
Revises: 2676fe99b0f5
Create Date: 2026-06-01 17:59:34.448583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee3263825627'
down_revision: Union[str, Sequence[str], None] = '2676fe99b0f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_index("idx_games_date", "games", ["date"], unique=False)

    op.create_index("idx_games_league_id", "games", ["league_id"], unique=False )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_games_league_id", table_name="games")
    op.drop_index("idx_games_date", table_name="games")
    pass
