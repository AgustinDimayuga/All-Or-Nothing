"""Cron_job

Revision ID: b3fa25d74754
Revises: 383d64614811
Create Date: 2026-05-09 18:31:50.881920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3fa25d74754'
down_revision: Union[str, Sequence[str], None] = '383d64614811'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


    # Enable pg_cron
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_cron;")


    # 1. Resolve games every 2 hours

    op.execute("""
        SELECT cron.schedule(
            'resolve-games-randomly',
            '0 */2 * * *',
            $$
            UPDATE games
            SET result = CASE
                WHEN RANDOM() < 0.5 THEN home_team_id
                ELSE away_team_id
            END
            WHERE date < NOW()
              AND result IS NULL;
            $$
        );
    """)


    # 2. Resolve bets every 1 hour

    op.execute("""
        SELECT cron.schedule(
            'resolve-bets',
            '0 * * * *',
            $$
            INSERT INTO wallet (user_id, from_bet, change)
            SELECT
                b.user_id,
                b.id,
                CASE
                    WHEN b.team_id = g.home_team_id THEN b.amount * g.home_odds
                    ELSE b.amount * g.away_odds
                END
            FROM bets b
            JOIN games g ON b.game_id = g.id
            WHERE b.resolved = FALSE AND g.result = b.team_id;


            UPDATE bets
            SET resolved = TRUE
            FROM games g
            WHERE bets.game_id = g.id
              AND bets.resolved = FALSE
              AND g.result = bets.team_id;
            $$
        );
    """)
    op.add_column("games", sa.Column("result", sa.Integer(),nullable=False))
    op.create_foreign_key("fk_results","games","teams",["results"],["team_id"])
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("SELECT cron.unschedule('resolve-games-randomly');")
    op.execute("SELECT cron.unschedule('resolve-bets');")
    op.execute("DROP EXTENSION IF EXISTS pg_cron;")

    pass
