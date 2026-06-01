"""1_million_rows

Revision ID: 4157d2058e87
Revises: 2676fe99b0f5
Create Date: 2026-05-29 23:23:41.143611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from faker import Faker
import numpy as np
import sqlalchemy
from src.api.user_helper import *
from src import database as db
import random
# revision identifiers, used by Alembic.
revision: str = '4157d2058e87'
down_revision: Union[str, Sequence[str], None] = '2676fe99b0f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    num_users = 100000
    fake = Faker()

    total_users = 0
    with db.engine.begin() as conn:
        print("creating fake Users...")
        posts = []
        for i in range(num_users):
            if (i % 1000 == 0):
                print(i)

            total_users += 1

            posts.append({
                "username": f"{fake.user_name()}_{i}" ,
                "name": fake.name(),
                "email":fake.unique.email(),
                "phone": fake.phone_number()[:20]

            })

        if posts:
            conn.execute(
            sqlalchemy.text("""
            INSERT INTO users (username, name, email, phone)
            VALUES (:username, :name, :email, :phone)
            """),
                posts,
            )

            print("total posts: ", total_users)
            print("after insert")

        user_ids= conn.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM users
                """
            )
        ).scalars().all()
        print("-------------------------------------------Making Wallets--------------------------------------------------------------")
        wallet =[]
        if user_ids:
            i=0
            for id in user_ids:
                if (i % 1000 == 0):
                    print(i)
                i+=1
                wallet.append({
                    "user_id":id,
                    "change":100000
                })
            if wallet:
                conn.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO wallet (user_id,change)
                        VALUES (:user_id,:change)
                        """
                    ),wallet
                )
        #   "created_at": fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None),

        teams= []
        games=[]
        total_games=0
        total_teams=0
        print("-------------------------------------------Making 50,000 Teams--------------------------------------------------------------")
        for i in range(50000):
            if i % 1000 == 0:
                print(i)
            total_teams+=1
            teams.append(
                {
                    "name":f"Team_{i}"
                }
            )
        if teams:
            conn.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO teams (name)
                    VALUES (:name)
                    """
                ),teams
            )

        print("-------------------------------------------Making 100,000 Games and leagues--------------------------------------------------------------")

        
        conn.execute(
        sqlalchemy.text(
            """
            INSERT INTO leagues (name, sport)
            VALUES
            ('world_cup', 'soccer'),
            ('nlb', 'baseball'),
            ('nba', 'basketball'),
            ('nfl', 'football'),
            ('nhl', 'hockey')
            """
        )
    )
        teams= conn.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM teams
                """
            )
        ).scalars().all()

        league_ids = conn.execute(
            sqlalchemy.text(
                """
                SELECT id 
                FROM leagues
                """
            )
        ).scalars().all()

        for i in range(100000):
            if i % 1000 == 0:
                print(i)
            total_teams+=1

            home = random.choice(teams)
            away = random.choice(teams)
            games.append(
                {
                    "league_id":random.choice(league_ids),
                    "home_team_id": home,
                    "away_team_id": away,
                    "date" : fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None),
                    "location": fake.location_on_land(),
                    "home_odds":random.uniform(0.5,3),
                    "away_odds":random.uniform(0.5,3),
                    "result": random.choice([home,away])
                }
            )
        if games:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO games (league_id,home_team_id,away_team_id,date,location,home_odds,away_odds,result)
                    VALUES (:league_id,:home_team_id,:away_team_id,:date,:location,:home_odds,:away_odds,:result)
                    """),
                games,
            )

        print("-------------------------------------------Making Bets--------------------------------------------------------------")

        game_ids =conn.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM games
                """
            )
        ).scalars().all()

        bets = []

        for user_id in user_ids:
            num_bets = random.randint(0, 20)  # each user has different activity level

            for _ in range(num_bets):
                game_id = random.choice(game_ids)
                
                #From the game that was selected choose a random team to bet on
                game = conn.execute(
                    sqlalchemy.text(
                        """
                        SELECT home_team_id, away_team_id
                        FROM games
                        WHERE id = :game_id
                        """
                    ),
                    {"game_id": game_id}
                ).mappings().one()

                team_id = random.choice([game["home_team_id"], game["away_team_id"]])

                bets.append({
                    "user_id": user_id,
                    "game_id": game_id,
                    "team_id": team_id,
                    "amount": round(random.uniform(5, 500), 2),
                    "resolved": True,
                    "created_at": fake.date_time_between(start_date='-2y', end_date='now')
                })

        if bets:
            conn.execute(
                sqlalchemy.text("""
                    INSERT INTO bets (user_id, game_id, team_id, amount, resolved, created_at)
                    VALUES (:user_id, :game_id, :team_id, :amount, :resolved, :created_at)
                """),
                bets,
            )

    pass


def downgrade() -> None:
    """Downgrade schema."""

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""TRUNCATE TABLE users RESTART IDENTITY CASCADE"""))
        connection.execute(sqlalchemy.text("""TRUNCATE TABLE teams RESTART IDENTITY CASCADE"""))
    pass
