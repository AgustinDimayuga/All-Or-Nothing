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
    # game_summary: str  # might remove
    team_bet_on: str
    amount: float
    odds: float
    potential_payout: float
    # status: str
    placed_at: str
    # new_balance: float  # Might be unnecessary


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


@router.post("/place", response_model=BetResponse)
def place_bet(user_id: int, bet_id: int, new_bet: Bet):
    with db.engine.begin() as connection:
        odds = 2

        team_id = connection.execute(
            sqlalchemy.text("""
                SELECT id
                FROM teams
                WHERE name = :name
                """),
            [{"name": new_bet.team}],
        ).scalar_one()

        placed_at = connection.execute(
            sqlalchemy.text("""
                INSERT INTO bets (user_id, game_id, team_id, amount, odds)
                VALUES (:user_id, :game_id, :team_id, :amount, :odds)
                RETURNING created_at
                """),
            [
                {
                    "user_id": user_id,
                    "game_id": new_bet.game_id,
                    "team_id": team_id,
                    "amount": new_bet.amount,
                    "odds": odds,
                }
            ],
        ).scalar_one()

        return BetResponse(
            bet_id=bet_id,
            game_id=new_bet.game_id,
            team_bet_on=new_bet.team,
            amount=new_bet.amount,
            odds=odds,
            potential_payout=odds * new_bet.amount,
            placed_at=placed_at,
        )
