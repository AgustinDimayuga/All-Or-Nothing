"""Insert values to table

Revision ID: 20a4a4724e51
Revises: 1e23635aa2fa
Create Date: 2026-05-04 22:10:26.261993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20a4a4724e51"
down_revision: Union[str, Sequence[str], None] = "1e23635aa2fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()

    league_id = bind.execute(
        sa.text("""
            INSERT INTO leagues (name, sport)
            VALUES (:name, :sport)
            RETURNING id
            """),
        [{"name": "NBA", "sport": "Basketball"}],
    ).scalar_one()

    team_id1 = bind.execute(
        sa.text("""
    INSERT INTO teams (league_id, name)
    VALUES (:league_id, :name)
    RETURNING id
    """),
        [{"league_id": league_id, "name": "Lakers"}],
    ).scalar_one()

    team_id2 = bind.execute(
        sa.text("""
    INSERT INTO teams (league_id, name)
    VALUES (:league_id, :name)
    RETURNING id
    """),
        [{"league_id": league_id, "name": "Warriors"}],
    ).scalar_one()

    team_id3 = bind.execute(
        sa.text("""
    INSERT INTO teams (league_id, name)
    VALUES (:league_id, :name)
    RETURNING id
    """),
        [{"league_id": league_id, "name": "Spurs"}],
    ).scalar_one()

    team_id4 = bind.execute(
        sa.text("""
    INSERT INTO teams (league_id, name)
    VALUES (:league_id, :name)
    RETURNING id
    """),
        [{"league_id": league_id, "name": "Wolves"}],
    ).scalar_one()

    bind.execute(
        sa.text("""
        INSERT INTO games (league_id, home_team_id, away_team_id, location, home_odds, away_odds)
        VALUES (:league_id, :home_team_id, :away_team_id, :location, :home_odds, :away_odds)
        """),
        [
            {
                "league_id": league_id,
                "home_team_id": team_id1,
                "away_team_id": team_id2,
                "location": "LA",
                "home_odds": 1.5,
                "away_odds": 2,
            }
        ],
    )

    bind.execute(
        sa.text("""
        INSERT INTO games (league_id, home_team_id, away_team_id, location, home_odds, away_odds)
        VALUES (:league_id, :home_team_id, :away_team_id, :location, :home_odds, :away_odds)
        """),
        [
            {
                "league_id": league_id,
                "home_team_id": team_id3,
                "away_team_id": team_id4,
                "location": "LA",
                "home_odds": 1.7,
                "away_odds": 2.3,
            }
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
