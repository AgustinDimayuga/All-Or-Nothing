"""add idempotency to bets

Revision ID: b23d884ca9f7
Revises: 1e23635aa2fa
Create Date: 2026-05-09 13:24:30.844044

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b23d884ca9f7"
down_revision: Union[str, Sequence[str], None] = "e34513c93c89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "new_bet_ids",
        sa.Column("bet_id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        "new_bets_user_fkey", "new_bet_ids", "users", ["user_id"], ["id"]
    )

    op.create_table(
        "processed_bets",
        sa.Column("bet_id", sa.Integer, primary_key=True),
        sa.Column("response", sa.Integer, nullable=False),
    )

    # op.add_column("bets", sa.Column("isWon", sa.Integer, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("new_bets_user_fkey", "new_bet_ids", type_="foreignkey")

    op.drop_table("new_bet_ids")
    op.drop_table("processed_bets")

    # op.drop_column("bets", "isWon")
