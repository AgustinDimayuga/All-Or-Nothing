"""add winners to games

Revision ID: c0e770eac2bb
Revises: 20a4a4724e51
Create Date: 2026-05-09 00:48:14.101773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0e770eac2bb'
down_revision: Union[str, Sequence[str], None] = '20a4a4724e51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("games", sa.Column("winning_team_id", sa.Integer(), nullable=True))

    op.create_foreign_key(
        "fk_games_winning_team_id",
        "games",
        "teams",
        ["winning_team_id"],
        ["id"],
        ondelete="SET NULL"
    )
    

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_games_winning_team_id", "games", type_="foreignkey")
    op.drop_column("games", "winning_team_id")
    
