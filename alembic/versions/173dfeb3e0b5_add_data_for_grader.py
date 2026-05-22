"""add data for grader

Revision ID: 173dfeb3e0b5
Revises: 383d64614811
Create Date: 2026-05-11 13:12:46.857696

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.api.auth import PostUser, create_user
from src.api.games import post_comment
from src.api.user_helper import get_password_hash, get_token_data

# revision identifiers, used by Alembic.
revision: str = "173dfeb3e0b5"
down_revision: Union[str, Sequence[str], None] = "4a4c3e3e5379"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sofia = PostUser(
        username="Sofia",
        name="Sofia",
        email="sofia@gmail.com",
        phone="714",
        password="string",
    )
    priya = PostUser(
        username="Priya",
        name="Priya",
        email="priya@gmail.com",
        phone="805",
        password="string",
    )
    derek = PostUser(
        username="Derek",
        name="Derek",
        email="derek@gmail.com",
        phone="801",
        password="string",
    )
    connection = op.get_bind()
    priya_hashed_password = get_password_hash(priya.password)
    sofia_hashed_password = get_password_hash(sofia.password)
    derek_hashed_password = get_password_hash(derek.password)

    priya_user_id = connection.execute(
        sa.text("""
        INSERT INTO users (username, name, email, phone)
        VALUES (:username, :name, :email, :phone)
        RETURNING id
        """),
        {
            "username": priya.username,
            "name": priya.name,
            "email": priya.email,
            "phone": priya.phone,
        },
    ).scalar_one()
    # Store password in user_creds
    connection.execute(
        sa.text("""
        INSERT INTO user_cred (user_id, password)
        VALUES (:user_id, :password)
        """),
        {"user_id": priya_user_id, "password": priya_hashed_password},
    )
    # Give user 100 dollars as a Bonus
    connection.execute(
        sa.text("""
            INSERT INTO wallet (user_id,change)
            VALUES(:user_id,:change)
        """),
        {"user_id": priya_user_id, "change": 100},
    )
    ############# SOFia
    sofia_user_id = connection.execute(
        sa.text("""
        INSERT INTO users (username, name, email, phone)
        VALUES (:username, :name, :email, :phone)
        RETURNING id
        """),
        {
            "username": sofia.username,
            "name": sofia.name,
            "email": sofia.email,
            "phone": sofia.phone,
        },
    ).scalar_one()
    # Store password in user_creds
    connection.execute(
        sa.text("""
        INSERT INTO user_cred (user_id, password)
        VALUES (:user_id, :password)
        """),
        {"user_id": sofia_user_id, "password": sofia_hashed_password},
    )
    # Give user 100 dollars as a Bonus
    connection.execute(
        sa.text("""
            INSERT INTO wallet (user_id,change)
            VALUES(:user_id,:change)
        """),
        {"user_id": sofia_user_id, "change": 100},
    )

    derek_user_id = connection.execute(
        sa.text("""
        INSERT INTO users (username, name, email, phone)
        VALUES (:username, :name, :email, :phone)
        RETURNING id
        """),
        {
            "username": derek.username,
            "name": derek.name,
            "email": derek.email,
            "phone": derek.phone,
        },
    ).scalar_one()
    # Store password in user_creds
    connection.execute(
        sa.text("""
        INSERT INTO user_cred (user_id, password)
        VALUES (:user_id, :password)
        """),
        {"user_id": derek_user_id, "password": derek_hashed_password},
    )
    # Give user 100 dollars as a Bonus
    connection.execute(
        sa.text("""
            INSERT INTO wallet (user_id,change)
            VALUES(:user_id,:change)
        """),
        {"user_id": derek_user_id, "change": 1000},
    )

    comment = connection.execute(
        sa.text("""
        INSERT INTO COMMENTS (user_id,body,game_id)
        VALUES (:user_id, :body,:game_id)
        RETURNING id, body, posted_at
        """),
        [
            {"user_id": derek_user_id, "body": "Yankees!!", "game_id": 1398},
            {"user_id": derek_user_id, "body": "Yankees rock!", "game_id": 1398},
            {"user_id": derek_user_id, "body": "Yankees!", "game_id": 1398},
            {"user_id": derek_user_id, "body": "Yankeeeeeeeeeees!", "game_id": 1398},
            {"user_id": sofia_user_id, "body": "Guardians!", "game_id": 1398},
            {
                "user_id": sofia_user_id,
                "body": "Guardians Are AMAZING!",
                "game_id": 1398,
            },
            {"user_id": sofia_user_id, "body": "Guardians ARE UP !", "game_id": 1398},
            {
                "user_id": sofia_user_id,
                "body": "Guardians GUARDIANS FOR LIFE !",
                "game_id": 1398,
            },
            {
                "user_id": sofia_user_id,
                "body": "Guardians! ALL THE WAY",
                "game_id": 1398,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
