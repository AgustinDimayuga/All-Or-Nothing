"""Updates_to_Nullable-Defaults

Revision ID: 31c2d62527a5
Revises: feb818e800a8
Create Date: 2026-05-04 13:47:17.318360

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "31c2d62527a5"
down_revision: Union[str, Sequence[str], None] = "feb818e800a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("fk_games_league_id", "games")
    op.drop_constraint("fk_games_home_team_id", "games")
    op.drop_constraint("fk_home_team_id", "games")
    op.drop_constraint("fk_league_id_teams", "teams")
    op.drop_constraint("fk_user_id-comments", "comments")
    op.drop_constraint("fk_parent_id", "comments")
    op.drop_constraint("fk_wallet_id", "users")
    op.drop_constraint("fk_user_id_wallet", "wallet")
    op.drop_constraint("fk_from_bet_bets", "wallet")
    op.drop_constraint("fk_user_id_bets", "bets")
    op.drop_constraint("fk_game_id_bets", "bets")
    op.drop_constraint("fk_team_id_bets", "bets")
    op.drop_constraint("fk_user_id", "user_cred")

    op.drop_table("users")
    op.drop_table("wallet")
    op.drop_table("bets")
    op.drop_table("games")
    op.drop_table("teams")
    op.drop_table("leagues")
    op.drop_table("comments")
    op.drop_table("user_cred")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, unique=True, nullable=False),
        sa.Column("wallet_id", sa.Integer, nullable=False),
        sa.Column("name", sa.Integer, nullable=True),
        sa.Column("email", sa.Integer, nullable=True),
        sa.Column("phone", sa.Integer, nullable=True),
        sa.Column(
            "user_created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    op.create_table(
        "user_cred",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("password", sa.String, nullable=False),
    )
    op.create_table(
        "wallet",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("from_bet", sa.Integer, nullable=True),
        sa.Column("change", sa.Integer, nullable=False),
    )
    op.create_table(
        "bets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("game_id", sa.Integer, nullable=False),
        sa.Column("team_id", sa.Integer, nullable=False),
        sa.Column("odds", sa.Integer, nullable=False),
        sa.Column("amount", sa.Integer, nullable=False),
        sa.Column(
            "resolved", sa.Boolean, server_default=sa.text("false"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_table(
        "games",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("league_id", sa.Integer, nullable=False),
        sa.Column("home_team_id", sa.Integer, nullable=False),
        sa.Column("away_team_id", sa.Integer, nullable=False),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("location", sa.String, nullable=False),
    )
    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("sport", sa.String, nullable=False),
    )
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("league_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String, nullable=False),
    )
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("parent_id", sa.Integer, nullable=False),
        sa.Column("body", sa.String, nullable=False),
        sa.Column(
            "posted_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    # 1. Foreign key from "leagues" to "games" to fullfill the league_id
    op.create_foreign_key(
        "fk_games_league_id",
        "games",
        "leagues",
        ["league_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 2. Foreign key from "teams" to "games" tp fullfill the home team id
    op.create_foreign_key(
        "fk_games_home_team_id",
        "games",
        "teams",
        ["home_team_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 3.Foreign key from "teams" to "games to fullfill the " away-teams-"id"
    op.create_foreign_key(
        "fk_home_team_id",
        "games",
        "teams",
        ["away_team_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 4. Foreign Key from "leagues" to teams to fulfill league_id column
    op.create_foreign_key(
        "fk_league_id_teams",
        "teams",
        "leagues",
        ["league_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 5. Foreign Key from "users" to "comments" to fulfill the user_id column
    op.create_foreign_key(
        "fk_user_id-comments",
        "comments",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 6. Foreign Key from "comments" to "comments" to create replies
    op.create_foreign_key(
        "fk_parent_id",
        "comments",
        "comments",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 7. Foreign Key from Wallet to Users to fulfill the "wallet_id" row
    op.create_foreign_key(
        "fk_wallet_id", "users", "wallet", ["wallet_id"], ["id"], ondelete="CASCADE"
    )

    # 8. Foreign Key from Users to Wallet to full fill the "user_id" row
    op.create_foreign_key(
        "fk_user_id_wallet", "wallet", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )

    # 9.Foriegn key from Bet to wallet to full fil the "from_bet key"
    op.create_foreign_key(
        "fk_from_bet_bets", "wallet", "bets", ["from_bet"], ["id"], ondelete="CASCADE"
    )

    # 10. Foreign Key From Users to Bets to full fill the "user_id" in bets
    op.create_foreign_key(
        "fk_user_id_bets", "bets", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )

    # 11 .Foreign Key from  Games to Bets to full fill the "game_id" row
    op.create_foreign_key(
        "fk_game_id_bets", "bets", "games", ["game_id"], ["id"], ondelete="CASCADE"
    )

    # 12 .Foreign Key from  Games to Bets to full fill the "game_id" row
    op.create_foreign_key(
        "fk_team_id_bets", "bets", "teams", ["team_id"], ["id"], ondelete="CASCADE"
    )

    # 13. Foreign key/Primary key for
    op.create_foreign_key(
        "fk_user_id", "user_cred", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_games_league_id", "games")
    op.drop_constraint("fk_games_home_team_id", "games")
    op.drop_constraint("fk_home_team_id", "games")
    op.drop_constraint("fk_league_id_teams", "teams")
    op.drop_constraint("fk_user_id-comments", "comments")
    op.drop_constraint("fk_parent_id", "comments")
    # op.drop_constraint("fk_wallet_id", "users")
    op.drop_constraint("fk_user_id_wallet", "wallet")
    op.drop_constraint("fk_from_bet_bets", "wallet")
    op.drop_constraint("fk_user_id_bets", "bets")
    op.drop_constraint("fk_game_id_bets", "bets")
    op.drop_constraint("fk_team_id_bets", "bets")
    op.drop_constraint("fk_user_id", "user_cred")

    op.drop_table("users")
    op.drop_table("wallet")
    op.drop_table("bets")
    op.drop_table("games")
    op.drop_table("teams")
    op.drop_table("leagues")
    op.drop_table("comments")
    op.drop_table("user_cred")
    pass
