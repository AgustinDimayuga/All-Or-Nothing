from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Double,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    UniqueConstraint,
    text,
)

metadata = MetaData()


t_leagues = Table(
    "leagues",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("sport", String, nullable=False),
    PrimaryKeyConstraint("id", name="leagues_pkey"),
)

t_users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("user_created_at", DateTime(True), server_default=text("now()")),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("phone", String(20), nullable=False),
    PrimaryKeyConstraint("id", name="users_pkey"),
    UniqueConstraint("username", name="users_username_key"),
)

t_comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("parent_id", Integer, nullable=False),
    Column("body", String, nullable=False),
    Column("posted_at", DateTime(True), nullable=False, server_default=text("now()")),
    ForeignKeyConstraint(
        ["parent_id"], ["comments.id"], ondelete="CASCADE", name="fk_parent_id"
    ),
    ForeignKeyConstraint(
        ["user_id"], ["users.id"], ondelete="CASCADE", name="fk_user_id-comments"
    ),
    PrimaryKeyConstraint("id", name="comments_pkey"),
)

t_teams = Table(
    "teams",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("league_id", Integer, nullable=False),
    Column("name", String, nullable=False),
    ForeignKeyConstraint(
        ["league_id"], ["leagues.id"], ondelete="CASCADE", name="fk_league_id_teams"
    ),
    PrimaryKeyConstraint("id", name="teams_pkey"),
)

t_user_cred = Table(
    "user_cred",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("password", String, nullable=False),
    ForeignKeyConstraint(
        ["user_id"], ["users.id"], ondelete="CASCADE", name="fk_user_id"
    ),
    PrimaryKeyConstraint("user_id", name="user_cred_pkey"),
)

t_games = Table(
    "games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("league_id", Integer, nullable=False),
    Column("home_team_id", Integer, nullable=False),
    Column("away_team_id", Integer, nullable=False),
    Column("date", DateTime(True), nullable=False, server_default=text("now()")),
    Column("location", String, nullable=False),
    Column("home_odds", Double(53), nullable=False),
    Column("away_odds", Double(53), nullable=False),
    ForeignKeyConstraint(
        ["away_team_id"], ["teams.id"], ondelete="CASCADE", name="fk_home_team_id"
    ),
    ForeignKeyConstraint(
        ["home_team_id"], ["teams.id"], ondelete="CASCADE", name="fk_games_home_team_id"
    ),
    ForeignKeyConstraint(
        ["league_id"], ["leagues.id"], ondelete="CASCADE", name="fk_games_league_id"
    ),
    PrimaryKeyConstraint("id", name="games_pkey"),
)

t_bets = Table(
    "bets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("game_id", Integer, nullable=False),
    Column("team_id", Integer, nullable=False),
    Column("amount", Integer, nullable=False),
    Column("resolved", Boolean, nullable=False, server_default=text("false")),
    Column("created_at", DateTime(True), nullable=False, server_default=text("now()")),
    ForeignKeyConstraint(
        ["game_id"], ["games.id"], ondelete="CASCADE", name="fk_game_id_bets"
    ),
    ForeignKeyConstraint(
        ["team_id"], ["teams.id"], ondelete="CASCADE", name="fk_team_id_bets"
    ),
    ForeignKeyConstraint(
        ["user_id"], ["users.id"], ondelete="CASCADE", name="fk_user_id_bets"
    ),
    PrimaryKeyConstraint("id", name="bets_pkey"),
)

t_wallet = Table(
    "wallet",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("from_bet", Integer),
    Column("change", Integer, nullable=False),
    ForeignKeyConstraint(
        ["from_bet"], ["bets.id"], ondelete="CASCADE", name="fk_from_bet_bets"
    ),
    ForeignKeyConstraint(
        ["user_id"], ["users.id"], ondelete="CASCADE", name="fk_user_id_wallet"
    ),
    PrimaryKeyConstraint("id", name="wallet_pkey"),
)
