from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Annotated

import sqlalchemy
from starlette import status

from src import database as db

router = APIRouter(
    prefix="/bets",
    tags=["bets"],
    # dependencies=[], //Add JWT
)


class Bet(BaseModel):
    game_id: int
    team: str
    amount: float


class BetResponse(BaseModel):
    bet_id: int
    game_id: int
    game_summary: str  # might remove
    team_bet_on: str
    amount: float
    odds: float
    potential_payout: float
    status: str
    placed_at: str
    new_balance: float  # Might be unnecessary


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_bet(user_id: int):
    with db.engine.begin() as connection:
        bet_id = connection.execute(
            sqlalchemy.text("""
                INSERT INTO new_bets (user_id)
                VALUES (:user_id)
                RETURNING bet_id
                """),
            [{"user_id": user_id}],
        ).scalar_one()

    return bet_id


# # Might remove but idk
# @router.post("/set", status_code=status.HTTP_201_CREATED)
# def set_bets(bet_id: int, bets: List[Bet]):
#     with db.engine.begin() as connection:
#         bet = connection.execute(
#             sqlalchemy.text("""
#                 SELECT *
#                 FROM bets
#                 WHERE bet_id = :bet_id
#                 """),
#             [{"bet_id": bet_id}],
#         ).one()
#
#      connection.execute(
#          sqlalchemy.text(
#              """
#              INSERT INTO
#              """
#          )
#      )
#     pass


@router.post("/place", response_model=BetResponse)
def place_bet(bet_id: int, new_bet: Bet):
    with db.engine.begin() as connection:
        existing_bet = connection.execute(
            sqlalchemy.text("""
            SELECT *
            FROM processed_bets
            WHERE bet_id = :bet_id
            """),
            [{"bet_id": bet_id}],
        )

        if existing_bet:
            return

        connection.execute(sqlalchemy.text("""
                INSERT INTO bets (bet_id, game_id, team_bet_on, amount, odds, potential_payout)
                VALUES ()
                """))

        odds = connection.execute(sqlalchemy.text("""
                SELECT odds
                FROM games
                WHERE game_id = :game_id
                """)).one()

        return BetResponse(
            bet_id=bet_id,
            game_id=new_bet.game_id,
            team_bet_on=new_bet.team,
            amount=new_bet.amount,
        )

    pass
