from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Annotated

import sqlalchemy

from src.api.user_helper import get_token_data, TokenData

from src import database as db

router = APIRouter(
    prefix="/bets", tags=["bets"], dependencies=[Depends(get_token_data)]
)


class Bet(BaseModel):
    game_id: int
    team: str
    amount: float


class BetResponse(BaseModel):
    bet_id: int
    game_id: int
    team_bet_on: str
    amount: float
    odds: float
    potential_payout: float
    status: str
    placed_at: str
    new_balance: float  # Might be unnecessary


# @router.post("/create", status_code=status.HTTP_201_CREATED)
# def create_bet(user_id: int):
#     with db.engine.begin() as connection:
#         bet_id = connection.execute(
#             sqlalchemy.text("""
#                 INSERT INTO new_bets (user_id)
#                 VALUES (:user_id)
#                 RETURNING bet_id
#                 """),
#             [{"user_id": user_id}],
#         ).scalar_one()
#
#     return bet_id


@router.post("/", response_model=BetResponse)
def place_bet(
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
    user_id: int,
    new_bet: Bet,
):
    if current_token_data.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Can only place bets on your account"
        )

    with db.engine.begin() as connection:

        cur_balance = connection.execute(
            sqlalchemy.text("""
                SELECT sum(change)
                FROM wallet
                WHERE user_id = :user_id
                """),
            [{"user_id": user_id}],
        ).scalar_one()

        if new_bet.amount > cur_balance:
            raise HTTPException(status_code=422, detail="Not enough money")

        odds = 2  # Hard code odds for now

        team_id = connection.execute(
            sqlalchemy.text("""
                SELECT id
                FROM teams
                WHERE name = :name
                """),
            [{"name": new_bet.team}],
        ).scalar_one()

        values = (
            connection.execute(
                sqlalchemy.text("""
                INSERT INTO bets (user_id, game_id, team_id, odds, amount)
                VALUES (:user_id, :game_id, :team_id, :odds, :amount)
                RETURNING id, created_at
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
            )
            .mappings()
            .one()
        )

        connection.execute(
            sqlalchemy.text("""
                INSERT INTO wallet (user_id, from_bet, change)
                VALUES (:user_id, :bet_id, :change)
                """),
            [
                {
                    "user_id": user_id,
                    "bet_id": values["id"],
                    "change": new_bet.amount * -1,
                }
            ],
        )

        return BetResponse(
            bet_id=values["id"],
            game_id=new_bet.game_id,
            team_bet_on=new_bet.team,
            amount=new_bet.amount,
            odds=odds,
            potential_payout=odds * new_bet.amount,
            status="active",
            placed_at=str(values["created_at"]),
            new_balance=cur_balance - new_bet.amount,
        )
